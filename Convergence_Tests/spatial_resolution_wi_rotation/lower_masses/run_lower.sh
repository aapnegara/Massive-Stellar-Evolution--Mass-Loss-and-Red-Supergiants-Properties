change() {
    # Modifies a parameter in the current inlist.
    # args: ($1) name of parameter
    #       ($2) new value
    #       ($3) filename of inlist where change should occur
    # Additionally changes the 'inlist_0all' inlist.
    # example command: change initial_mass 1.3
    # example command: change log_directory 'LOGS_MS'
    # example command: change do_element_diffusion .true.
    param=$1
    newval=$2
    filename=$3
    escapedParam=$(sed 's/[^^]/[&]/g; s/\^/\\^/g' <<< "$param")
    search="^\s*\!*\s*$escapedParam\s*=.+$"
    replace="      $param = $newval"
    sed -r -i.bak -e "s/$search/$replace/g" $filename
}

v_rot_ZAMS_array=(273 265) #271 262
ZFN_array=("'z0014_y0266_ekstrom_15.data'" "'z0014_y0266_ekstrom_12.data'")
M_ZAMS_array=(15 12)

for vc in 1e-5 1e-4; do
for dq in 0.0005 0.0001 0.005 0.001; do
for i in 0 1; do

	change 'max_dq' $dq 'inlist_massive_defaults'
	change 'varcontrol_target' $vc 'inlist_massive_defaults'
	change 'initial_mass' ${M_ZAMS_array[i]} 'inlist_star'
	change 'zams_filename' ${ZFN_array[i]} 'inlist_star'
	change 'new_surface_rotation_v' ${v_rot_ZAMS_array[i]} 'inlist_star'
	change 'log_directory' "'LOGS_${M_ZAMS_array[i]}M0_dq${dq}_vc${vc}'" 'inlist_star'
	change 'photo_directory' "'photos_${M_ZAMS_array[i]}M0_dq${dq}_vc${vc}'" 'inlist_star'

    if [ -d LOGS_${M_ZAMS_array[i]}M0_dq${dq}_vc${vc} ]; then
        cd LOGS_${M_ZAMS_array[i]}M0_dq${dq}_vc${vc}
	    gvfs-trash *
	    cd ../
    fi
    if [ -d photos_${M_ZAMS_array[i]}M0_dq${dq}_vc${vc} ]; then
        cd photos_${M_ZAMS_array[i]}M0_dq${dq}_vc${vc}
	    gvfs-trash *
	    cd ../
    fi
	./mk
	./rn
done
done
done