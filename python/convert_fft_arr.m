load('python_fft_export.mat');

num_samples = length(fft_data);
dt = 1; 
t = (0:num_samples-1)' * dt;

ts_data = timeseries(fft_data, t);

save('prn_fft.mat', 'ts_data', '-v7.3');
