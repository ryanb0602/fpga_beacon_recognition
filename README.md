# FPGA beacon recognition

This is a model for acquisition of coexistence beacons based on GNSS-like phase modulated waveforms made in CASPER using Vitis HLS.

To build follow these steps:

Navigate to the gnss_corr_hls folder

Run:
vitis run_hls.tcl

Navigate to the peak_finder_hls folder

Run:
vitis run_hls.tcl

Navigate to the CASPER directory, run startsg startsg.local

Load the pre generated file to matlab and open the simulink project

In the simulink project, make sure the HLS blocks point to the generated HLS solution directories

Run jasper in matlab
