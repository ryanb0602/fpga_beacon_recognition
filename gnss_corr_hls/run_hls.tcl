open_project gnss_corr_proj
set_top gnss_correlator
add_files gnss_correlator.cpp
add_files -tb tb_gnss_correlator.cpp
open_solution "sol1"
set_part {xc7z020clg400-1}   ;# use your actual part
create_clock -period 10
csim_design                  ;# <-- this runs the C simulation / testbench
csynth_design              ;# uncomment to synthesize
# cosim_design               ;# uncomment for RTL co-simulation
exit
