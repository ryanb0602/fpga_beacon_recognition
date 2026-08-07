# /outputs

The outputs folder containers the last generated working binarys for this project. This was used for the demonstration with helperscript gps_corr_new.py

Names for inputs in this are intended to make it easy to tell what is what, especially when referenced against the simulink design. Use fpga.listdev() for a better understanding.

In the demonstration, fir1 gain was set to 2, fir2 0, fir3 0. Accum, 200 frames.

# Simulink Model

The simulink model requires some matlab variables to use. These are all put into the pregenerated file, but can also be regenerated if need be. The tap generating scripts were modified from the version given by John Swoboda to fit this project. The gc_real and complex arrays are the arrays of the fft conjugates of the target gold codes. In the future, a better version of this project would load these through a software addresable bram or other interface to allow searching through a code space. (Or integrate a code space search into the design) Chipped test wave and phase shift test are arrays that load the testing ROMs. These allow for the test modes implemented in this project. The chipped test wave as implemented right now is real values that when fed through the digital downsampler should output a 0, 1 pattern of IQ data. The phase shift test should output a known phase shift bin of 500. (i think)

The user will also need to regenerate the hls modules. This can be done by pointing Vitis at the tcl scripts included, then pointing the simulink hls blocks at the solution folder
