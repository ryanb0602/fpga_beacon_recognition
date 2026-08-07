#include "gnss_correlator.hpp"
#include <cmath>
#include <cstdio>
#include <cstdlib>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

static void ref_dft(const std::complex<double> in[FFT_LEN],
                    std::complex<double> out[FFT_LEN]) {
  for (unsigned k = 0; k < FFT_LEN; k++) {
    std::complex<double> acc(0, 0);
    for (unsigned n = 0; n < FFT_LEN; n++) {
      double a = -2.0 * M_PI * k * n / FFT_LEN;
      acc += in[n] * std::complex<double>(std::cos(a), std::sin(a));
    }
    out[k] = acc;
  }
}

int main() {
  const unsigned D = 1000;               // True Code Delay
  const double FS = 4096000.0;           // Sampling rate (Hz)
  const double TRUE_DOPPLER_HZ = 1500.0; // True incoming Doppler shift (Hz)

  // Doppler search grid configuration
  const double DOPPLER_MIN_HZ = -5000.0;
  const double DOPPLER_MAX_HZ = 5000.0;
  const double DOPPLER_STEP_HZ = 250.0;

  const int NUM_FRAMES =
      2; // Run frames to allow continuous pipeline processing

  // 1. Generate baseband PRN code sequence
  std::complex<double> code_d[FFT_LEN];
  for (unsigned n = 0; n < FFT_LEN; n++) {
    double bit = (std::rand() & 1) ? 0.5 : -0.5;
    code_d[n] = std::complex<double>(bit, 0.0);
  }

  // 2. Reference DFT and local code replica (frequency domain conjugate)
  std::complex<double> C[FFT_LEN];
  ref_dft(code_d, C);

  double cmax = 0.0;
  for (unsigned k = 0; k < FFT_LEN; k++) {
    double m = std::abs(C[k]);
    if (m > cmax)
      cmax = m;
  }

  fft_data_t code_re_arr[FFT_LEN], code_im_arr[FFT_LEN];
  for (unsigned k = 0; k < FFT_LEN; k++) {
    std::complex<double> cc = std::conj(C[k]) / (cmax * 1.01);
    code_re_arr[k] = (fft_data_t)cc.real();
    code_im_arr[k] = (fft_data_t)cc.imag();
  }

  // 3. Open CSV file to dump 2D search matrix
  FILE *fp = fopen("gnss_search_space.csv", "w");
  if (!fp) {
    printf("Error: Could not open gnss_search_space.csv for writing.\n");
    return 1;
  }
  fprintf(fp, "doppler_hz,lag,magnitude\n");

  hls::stream<fft_data_t> stream_iq_re("iq_re");
  hls::stream<fft_data_t> stream_iq_im("iq_im");
  hls::stream<fft_data_t> stream_corr_re("corr_re");
  hls::stream<fft_data_t> stream_corr_im("corr_im");

  double global_max_mag = -1.0;
  double global_best_doppler = 0.0;
  unsigned global_best_lag = 0;

  printf("Starting 2D GNSS Acquisition Search (Doppler: [%.0f, %.0f] Hz)...\n",
         DOPPLER_MIN_HZ, DOPPLER_MAX_HZ);

  // 4. Sweep Doppler candidate frequencies
  for (double f_cand = DOPPLER_MIN_HZ; f_cand <= DOPPLER_MAX_HZ;
       f_cand += DOPPLER_STEP_HZ) {
    // Residual carrier frequency after candidate wipe-off
    double f_res = TRUE_DOPPLER_HZ - f_cand;

    // Load frames with incoming signal modulated by residual Doppler
    for (int f = 0; f < NUM_FRAMES; f++) {
      for (unsigned n = 0; n < FFT_LEN; n++) {
        unsigned src = (n + FFT_LEN - D) % FFT_LEN;

        // Continuous time index across frame boundaries
        double t = (double)(f * FFT_LEN + n) / FS;
        double phase = 2.0 * M_PI * f_res * t;

        // Apply carrier phase modulation
        double i_sig = code_d[src].real() * std::cos(phase) -
                       code_d[src].imag() * std::sin(phase);
        double q_sig = code_d[src].real() * std::sin(phase) +
                       code_d[src].imag() * std::cos(phase);

        stream_iq_re.write((fft_data_t)i_sig);
        stream_iq_im.write((fft_data_t)q_sig);
      }
    }

    // Run DUT consecutively for each frame
    for (int f = 0; f < NUM_FRAMES; f++) {
      gnss_correlator(stream_iq_re, stream_iq_im, code_re_arr, code_im_arr,
                      stream_corr_re, stream_corr_im);
    }

    // Process correlator output streams
    for (int f = 0; f < NUM_FRAMES; f++) {
      for (unsigned n = 0; n < FFT_LEN; n++) {
        double re_val = (double)stream_corr_re.read();
        double im_val = (double)stream_corr_im.read();
        double m = std::sqrt(re_val * re_val + im_val * im_val);

        // Record the last frame to eliminate startup transients
        if (f == (NUM_FRAMES - 1)) {
          fprintf(fp, "%.2f,%u,%.6f\n", f_cand, n, m);

          if (m > global_max_mag) {
            global_max_mag = m;
            global_best_doppler = f_cand;
            global_best_lag = n;
          }
        }
      }
    }
  }

  fclose(fp);

  printf("\n=== ACQUISITION SEARCH COMPLETE ===\n");
  printf("Target True Peak : Doppler = %.1f Hz, Lag = %u\n", TRUE_DOPPLER_HZ,
         D);
  printf("Acquired Peak    : Doppler = %.1f Hz, Lag = %u (Mag = %.6f)\n",
         global_best_doppler, global_best_lag, global_max_mag);

  if (global_best_lag == D &&
      std::abs(global_best_doppler - TRUE_DOPPLER_HZ) < DOPPLER_STEP_HZ) {
    printf("*** TEST PASSED: Peak located at correct Doppler & Code Lag ***\n");
    return 0;
  } else {
    printf("*** TEST FAILED: Peak position incorrect ***\n");
    return 1;
  }
}
