! ***********************************************************************
!
!   Copyright (C) 2011  Bill Paxton
!
!   this file is part of mesa.
!
!   mesa is free software; you can redistribute it and/or modify
!   it under the terms of the gnu general library public license as published
!   by the free software foundation; either version 2 of the license, or
!   (at your option) any later version.
!
!   mesa is distributed in the hope that it will be useful, 
!   but without any warranty; without even the implied warranty of
!   merchantability or fitness for a particular purpose.  see the
!   gnu library general public license for more details.
!
!   you should have received a copy of the gnu library general public license
!   along with this software; if not, write to the free software
!   foundation, inc., 59 temple place, suite 330, boston, ma 02111-1307 usa
!
! ***********************************************************************
 
      module run_star_extras

      use star_lib
      use star_def
      use const_def
      use chem_def, only: ih1, ih2, ihe3, ihe4
      
      implicit none
      
      integer :: time0, time1, clock_rate

	type (star_info), pointer :: s

	real(dp) :: mdot_timescale
      
      ! these routines are called by the standard run_star check_model
      contains
      
	subroutine  V_dJ_M_wind(id, Lsurf, Msurf, Rsurf, Tsurf, w, ierr)                                                                  
	     use crlibm_lib                                                                                                                    
	     type (star_info), pointer :: s                                                                                                                      
	     integer, intent(in) :: id                                                                                                                           
	     real(dp), intent(in) :: Lsurf, Msurf, Rsurf, Tsurf ! surface values (cgs)                                                                           
	     ! NOTE: surface is outermost cell. not necessarily at photosphere.                                                                                  
	     ! NOTE: don't assume that vars are set at this point.                                                                                               
	     ! so if you want values other than those given as args,                                                                                             
	     ! you should use values from s% xh(:,:) and s% xa(:,:) only.                                                                                        
	     ! rather than things like s% Teff or s% lnT(:) which have not been set yet.                                                                         
	     real(dp), intent(out) :: w ! wind in units of Msun/year (value is >= 0)                                                                             
	     integer, intent(out) :: ierr                                                                                                                        
	     real(dp) ::  L1, M1, R1, T1, xsurf, etaCOOL, etaHOT, etaWARM, Zsolar, Y, Z
	     real(dp) :: log10w, w1, w2, T_high, T_low, alfa
	     call get_star_ptr(id,s,ierr)                                                                                                                
	     w = 0                                                                                                                                       
	     ierr = 0                                                                                                                                    
	     L1 = Lsurf                                                                                                                                  
	     M1 = Msurf                                                                                                                                  
	     R1 = Rsurf                                                                                                                                  
	     T1 = Tsurf                                                                                                                                  
	     Zsolar = 0.019         
	     !I use the same factor everywhere                          
	     etaHOT = s% x_ctrl(1)
	     etaWARM = s% x_ctrl(2)
	     etaCOOL = s% x_ctrl(3) 
	     !Assumes the use of approx21.net           
	     !xsurf = s%xa(s%net_iso(iprot), 1)+ s%xa(s%net_iso(ih1), 1) !H mass fraction of the outermost cell, species 1 being neutrons                                                         
	     ! Assumes to NOT use approx* family of networks
	     T_high = 11000d0                                                                                                                              
	     T_low = 10000d0     

	        
	if (T1 < 5012) then                                                                                                            
                print *, 'using: Meynet_wind, eta=', etaCOOL
	       call eval_Meynet_wind(w)
	       w = w * etaCOOL            

	else if (T1 < 7943) then      
                print *, 'using: de_Jager, eta=', etaWARM
                call eval_de_Jager_wind(w)                                                                                                               
                w = w * etaWARM
        else                           
                print *, 'using: Vink, eta=', etaHOT
                call eval_vink_wind(w)                                                                                                            
                w = w * etaHOT
        end if 
	
	! mdot x3 if L > 5*Ledd (for M > 20M0)
	if (L1 > 5 * s% prev_Ledd) then
		w = w * 3
		print *, 'Super Eddington Boost!'
	end if

	print *, 'L/Ledd = ', L1/ s% prev_Ledd
	
         contains
           	
        subroutine eval_de_Jager_wind(w)
        ! de Jager, C., Nieuwenhuijzen, H., & van der Hucht, K. A. 1988, A&AS, 72, 259.                                             
         real(dp), intent(out) :: w
            real(dp) :: log10w
            include 'formats'
            log10w = 1.769d0*log10_cr(L1/Lsun) - 1.676d0*log10_cr(T1) - 8.158d0                                                                             
            w = exp10_cr(log10w)
         end subroutine eval_de_Jager_wind

	subroutine eval_Meynet_wind(w)
        ! From Meynet et al. 2015
         real(dp), intent(out) :: w
            real(dp) :: log10w
            include 'formats'
            log10w = log10_cr(L1/Lsun)*1.77 - 13.79                                                                              
            w = exp10_cr(log10w)
         end subroutine eval_Meynet_wind


	subroutine eval_vink_wind(w)
            real(dp), intent(inout) :: w
            real(dp) :: alfa, w1, w2, Teff_jump, logMdot, dT, vinf_div_vesc
	   Zsolar = 0.019d0 ! for Vink et al formula                                                                                            
	   xsurf = s%xa(s%net_iso(ih1), 1) !+ s%xa(s%net_iso(ih2), 1) !H2 not on current net
            Y = s% xa(s%net_iso(ihe3),1) + s% xa(s%net_iso(ihe4),1)                                                                 
            Z = 1 - Y -xsurf   

            ! alfa = 1 for hot side, = 0 for cool side
            if (T1 > 27500) then
               alfa = 1
            else if (T1 < 22500) then
               alfa = 0
            else ! use Vink et al 2001, eqns 14 and 15 to set "jump" temperature
               Teff_jump = 1d3*(61.2d0 + 2.59d0*(-13.636d0 + 0.889d0*log10_cr(Z/Zsolar)))
               dT = 100d0
               if (T1 > Teff_jump + dT) then
                  alfa = 1
               else if (T1 < Teff_jump - dT) then
                  alfa = 0
               else
                  alfa = (T1 - (Teff_jump - dT)) / (2*dT)
		print *, alfa
               end if
            end if

            if (alfa > 0) then ! eval hot side wind (eqn 24)
               vinf_div_vesc = 2.6d0 ! this is the hot side galactic value
               vinf_div_vesc = vinf_div_vesc*pow_cr(Z/Zsolar,0.13d0) ! corrected for Z  
               logMdot = &
                  - 6.697d0 &
                  + 2.194d0*log10_cr(L1/Lsun/1d5) &
                  - 1.313d0*log10_cr(M1/Msun/30) &
                  - 1.226d0*log10_cr(vinf_div_vesc/2d0) &
                  + 0.933d0*log10_cr(T1/4d4) &
                  - 10.92d0*pow2(log10_cr(T1/4d4)) &
                  + 0.85d0*log10_cr(Z/Zsolar)
               w1 = exp10_cr(logMdot)
            else
               w1 = 0
            end if

            if (alfa < 1) then ! eval cool side wind (eqn 25)
               vinf_div_vesc = 1.3d0 ! this is the cool side galactic value
               vinf_div_vesc = vinf_div_vesc*pow_cr(Z/Zsolar,0.13d0) ! corrected for Z
               logMdot = &
                  - 6.688d0 &
                  + 2.210d0*log10_cr(L1/Lsun/1d5) &
                  - 1.339d0*log10_cr(M1/Msun/30) &
                  - 1.601d0*log10_cr(vinf_div_vesc/2d0) &
                  + 1.07d0*log10_cr(T1/2d4) &
                  + 0.85d0*log10_cr(Z/Zsolar)
               w2 = exp10_cr(logMdot)
            else
               w2 = 0
            end if

            w = alfa*w1 + (1 - alfa)*w2

         end subroutine eval_vink_wind



      end subroutine V_dJ_M_wind


      subroutine extras_controls(id, ierr)
         integer, intent(in) :: id
         integer, intent(out) :: ierr
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         
         s% other_wind => V_dJ_M_wind     
         s% extras_startup => extras_startup
         s% extras_check_model => extras_check_model
         s% extras_finish_step => extras_finish_step
         s% extras_after_evolve => extras_after_evolve
         s% how_many_extra_history_columns => how_many_extra_history_columns
         s% data_for_extra_history_columns => data_for_extra_history_columns
         s% how_many_extra_profile_columns => how_many_extra_profile_columns
         s% data_for_extra_profile_columns => data_for_extra_profile_columns  
      end subroutine extras_controls
      
      
      integer function extras_startup(id, restart, ierr)
         integer, intent(in) :: id
         logical, intent(in) :: restart
         integer, intent(out) :: ierr
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         extras_startup = 0
         call system_clock(time0,clock_rate)
         if (.not. restart) then
            call alloc_extra_info(s)
         else ! it is a restart
            call unpack_extra_info(s)
         end if
      end function extras_startup
      
      
      subroutine extras_after_evolve(id, id_extra, ierr)
         integer, intent(in) :: id, id_extra
         integer, intent(out) :: ierr
         type (star_info), pointer :: s
         double precision :: dt
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         call system_clock(time1,clock_rate)
         dt = dble(time1 - time0) / clock_rate / 60
         write(*,'(/,a50,f12.2,99i10/)') 'runtime (minutes), retries, backups, steps', &
            dt, s% num_retries, s% num_backups, s% model_number
         ierr = 0
      end subroutine extras_after_evolve
      

      ! returns either keep_going, retry, backup, or terminate.
      integer function extras_check_model(id, id_extra)
         integer, intent(in) :: id, id_extra
         integer :: ierr
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         extras_check_model = keep_going         
      end function extras_check_model


      integer function how_many_extra_history_columns(id, id_extra)
         integer, intent(in) :: id, id_extra
         integer :: ierr
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         how_many_extra_history_columns = 0
      end function how_many_extra_history_columns
      
      
      subroutine data_for_extra_history_columns(id, id_extra, n, names, vals, ierr)
         integer, intent(in) :: id, id_extra, n
         character (len=maxlen_history_column_name) :: names(n)
         real(dp) :: vals(n)
         integer, intent(out) :: ierr
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
      end subroutine data_for_extra_history_columns

      
      integer function how_many_extra_profile_columns(id, id_extra)
         use star_def, only: star_info
         integer, intent(in) :: id, id_extra
         integer :: ierr
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         how_many_extra_profile_columns = 0
      end function how_many_extra_profile_columns
      
      
      subroutine data_for_extra_profile_columns(id, id_extra, n, nz, names, vals, ierr)
         use star_def, only: star_info, maxlen_profile_column_name
         use const_def, only: dp
         integer, intent(in) :: id, id_extra, n, nz
         character (len=maxlen_profile_column_name) :: names(n)
         real(dp) :: vals(nz,n)
         integer, intent(out) :: ierr
         type (star_info), pointer :: s
         integer :: k
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
      end subroutine data_for_extra_profile_columns

!=============================================================================================================      

      ! returns either keep_going or terminate.
      integer function extras_finish_step(id, id_extra)
         use crlibm_lib
         integer, intent(in) :: id, id_extra
         integer :: ierr, k
         type (star_info), pointer :: s
         real(dp) :: time, mdot_timescale, xsurf

         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         extras_finish_step = keep_going
         call store_extra_info(s)

	call system_clock(time1,clock_rate)
         time = dble(time1-time0)/ clock_rate / 60 ! elapsed time in minutes
         extras_finish_step = keep_going
         call store_extra_info(s)

         if (time .GT. 1435) then !715 min = 11h:55min
            extras_finish_step = terminate
            print *, 'Terminated because maximum time reached'
         end if
         call get_star_ptr(id,s,ierr)       
         
         !control that the next timestep is smaller than the relevant timescales!                                                                               
       
         mdot_timescale = s% mstar / (1d0 * abs(s% mstar_dot)) ! in sec
         print *, "proposed dt_next [yr]", s% dt_next / secyer
        !dt_next must be in seconds, but for numerical stability the min
        ! must be evaluated with stuff in years
         s% dt_next = min(s% dt_next / secyer , s% kh_timescale, mdot_timescale / secyer)
         s% dt_next = s% dt_next * secyer

         if (min(s% dt_next / secyer , s% kh_timescale, &
              mdot_timescale / secyer) & 
              == s% kh_timescale ) then
            print *, "dt_next limited by kh_timescale"
         else if (min(s% dt_next / secyer , s% kh_timescale, &
              mdot_timescale / secyer) &
              == mdot_timescale / secyer )  then
            print *, "dt_next limited by mdot_timescale"
         end if

	if (s% dt_next/secyer .gt. 1d6) then
	   print *, "dt larger than 10000 years"
	end if
                  
         if (extras_finish_step == terminate) s% termination_code = t_extras_finish_step
   end function extras_finish_step

!=============================================================================================================      
      
      ! routines for saving and restoring extra data so can do restarts
         
         ! put these defs at the top and delete from the following routines
         !integer, parameter :: extra_info_alloc = 1
         !integer, parameter :: extra_info_get = 2
         !integer, parameter :: extra_info_put = 3
      
      
      subroutine alloc_extra_info(s)
         integer, parameter :: extra_info_alloc = 1
         type (star_info), pointer :: s
         call move_extra_info(s,extra_info_alloc)
      end subroutine alloc_extra_info
      
      
      subroutine unpack_extra_info(s)
         integer, parameter :: extra_info_get = 2
         type (star_info), pointer :: s
         call move_extra_info(s,extra_info_get)
      end subroutine unpack_extra_info
      
      
      subroutine store_extra_info(s)
         integer, parameter :: extra_info_put = 3
         type (star_info), pointer :: s
         call move_extra_info(s,extra_info_put)
      end subroutine store_extra_info
      
      
      subroutine move_extra_info(s,op)
         integer, parameter :: extra_info_alloc = 1
         integer, parameter :: extra_info_get = 2
         integer, parameter :: extra_info_put = 3
         type (star_info), pointer :: s
         integer, intent(in) :: op
         
         integer :: i, j, num_ints, num_dbls, ierr
         
         i = 0
         ! call move_int or move_flg    
         num_ints = i
         
         i = 0
         ! call move_dbl       
         
         num_dbls = i
         
         if (op /= extra_info_alloc) return
         if (num_ints == 0 .and. num_dbls == 0) return
         
         ierr = 0
         call star_alloc_extras(s% id, num_ints, num_dbls, ierr)
         if (ierr /= 0) then
            write(*,*) 'failed in star_alloc_extras'
            write(*,*) 'alloc_extras num_ints', num_ints
            write(*,*) 'alloc_extras num_dbls', num_dbls
            stop 1
         end if
         
!==========================================================================================


!=============================================================================================================

         contains
         
         subroutine move_dbl(dbl)
            double precision :: dbl
            i = i+1
            select case (op)
            case (extra_info_get)
               dbl = s% extra_work(i)
            case (extra_info_put)
               s% extra_work(i) = dbl
            end select
         end subroutine move_dbl
         
         subroutine move_int(int)
            integer :: int
            i = i+1
            select case (op)
            case (extra_info_get)
               int = s% extra_iwork(i)
            case (extra_info_put)
               s% extra_iwork(i) = int
            end select
         end subroutine move_int
         
         subroutine move_flg(flg)
            logical :: flg
            i = i+1
            select case (op)
            case (extra_info_get)
               flg = (s% extra_iwork(i) /= 0)
            case (extra_info_put)
               if (flg) then
                  s% extra_iwork(i) = 1
               else
                  s% extra_iwork(i) = 0
               end if
            end select
         end subroutine move_flg
      
      end subroutine move_extra_info

      end module run_star_extras
      
