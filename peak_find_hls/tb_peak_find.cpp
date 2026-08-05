#include "peak_find.hpp"
#include <cstdlib>
#include <iostream>

int main() {
  hls::stream<fp_data> iq_re_stream("iq_re");
  hls::stream<fp_data> iq_im_stream("iq_im");

  unsigned int target_accum_frames = 5;

  // Outputs
  unsigned int peak_index = 0;
  accum_type peak_value = 0;
  accum_type noise_mean = 0;

  // The known index where we will inject an artificially high signal
  const unsigned int INJECTED_PEAK_INDEX = 500;

  std::cout << "Starting PCPS Accumulator Testbench..." << std::endl;

  // Because the HLS block processes 1 frame per execution,
  // we must call it 'target_accum_frames' times.
  for (unsigned int frame = 0; frame < target_accum_frames; frame++) {

    // 1. Generate 1 frame of dummy data
    for (unsigned int i = 0; i < ARRAY_SIZE; i++) {
      fp_data i_val, q_val;

      if (i == INJECTED_PEAK_INDEX) {
        // Inject a strong signal at index 500 (e.g., 0.5 + 0.5j)
        i_val = 0.5;
        q_val = 0.5;
      } else {
        // Inject low-level background noise (approx 0.05)
        // rand() is used just to give some variance to the noise
        i_val = 0.05 * ((rand() % 10) / 10.0);
        q_val = 0.05 * ((rand() % 10) / 10.0);
      }

      iq_re_stream.write(i_val);
      iq_im_stream.write(q_val);
    }

    // 2. Call the hardware function for this frame
    peak_find(iq_re_stream, iq_im_stream, target_accum_frames, peak_index,
              peak_value, noise_mean);

    std::cout << "Processed Frame " << frame + 1 << "/" << target_accum_frames
              << std::endl;
  }

  // 3. Verify the results
  std::cout << "-----------------------------------" << std::endl;
  std::cout << "Testbench Results:" << std::endl;
  std::cout << "Found Peak at Index : " << peak_index
            << " (Expected: " << INJECTED_PEAK_INDEX << ")" << std::endl;
  std::cout << "Peak Magnitude Val  : " << peak_value << std::endl;
  std::cout << "Mean Noise Level    : " << noise_mean << std::endl;

  // Simple software-side CFAR SNR calculation
  float snr = (float)peak_value / (float)noise_mean;
  std::cout << "Calculated SNR      : " << snr << std::endl;

  if (peak_index == INJECTED_PEAK_INDEX && snr > 10.0) {
    std::cout << "STATUS: PASS" << std::endl;
    return 0; // 0 means success in C++ testbenches
  } else {
    std::cout << "STATUS: FAIL" << std::endl;
    return 1;
  }
}
