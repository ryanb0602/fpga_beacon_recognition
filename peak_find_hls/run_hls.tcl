open_project peak_find_proj
set_top peak_find
add_files peak_find.cpp
add_files -tb tb_peak_find.cpp
open_solution "sol1"
set_part {xczu48dr-ffvg1517-1-e}
create_clock -period 3.7 ;#ns

csim_design                  ;# Runs C simulation and generates CSV
csynth_design                ;# Synthesizes C++ to RTL
#export_design -format syn_dcp
#export_design -format ip_catalog -output ./peak_find_ip

export_design -format sysgen

#cosim_design               ;# uncomment for RTL co-simulation
exit
