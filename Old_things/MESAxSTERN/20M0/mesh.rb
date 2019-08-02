load '../../../utils/plot_by_name.rb'

data_dir = 'mesh_plot_data'
logfile = 'new_mesh.data'
namesfile = 'new_mesh.names'
Plot_by_Name.make_names(logfile,namesfile,data_dir) # create names file from names on first line of log file
Plot_by_Name.new(
   'xaxis_column' => 'k', 'reverse_xaxis' => true,
   #'xaxis_column' => 'mass', 'reverse_xaxis' => false,
   'first' => 0, 'last' => -1, 
   #'first' => -50, 'last' => -1, 
   #'first' => 1531, 'last' => 1544, 
   'data_dir' => data_dir, 'lines_before_real_data' => 1,
   'test_file' => logfile, 'names_file' => namesfile
   )
