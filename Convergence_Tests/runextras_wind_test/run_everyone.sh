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
#from https://github.com/earlbellinger

./mk

for delta in 0.5 1.0 1.5 2.0; do
    for varc in 1e-5 1e-4 1e-3; do
	echo $delta
	echo $varc
	change 'mesh_delta_coeff' $delta 'inlist_32M0'
	change 'varcontrol_target' $varc 'inlist_32M0'
	change 'log_directory' "'LOGS_m$delta""_v$varc'" 'inlist_32M0'
	change 'photo_directory' "'photos_m$delta""_v$varc'" 'inlist_32M0'
    	./rn
    done
done
