open_project gnss_corr_proj
set_top gnss_correlator
add_files gnss_correlator.cpp
add_files -tb tb_full_search.cpp
open_solution "sol1"
set_part {xczu48dr-ffvg1517-1-e}
create_clock -period 3.7

csim_design                  ;# Runs C simulation and generates CSV
#csynth_design                ;# Synthesizes C++ to RTL
#export_design -format syn_dcp
#export_design -format ip_catalog -output ./gnss_correlator_ip

#export_design -format sysgen

#cosim_design               ;# uncomment for RTL co-simulation
exit
