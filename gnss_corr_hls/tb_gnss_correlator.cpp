// tb_gnss_correlator.cpp
#include "gnss_correlator.hpp"
#include <cmath>
#include <cstdio>
#include <cstdlib>

static void ref_dft(const std::complex<double> in[FFT_LEN],
                    std::complex<double> out[FFT_LEN]) {
  const double PI = 3.14159265358979323846;
  for (unsigned k = 0; k < FFT_LEN; k++) {
    std::complex<double> acc(0, 0);
    for (unsigned n = 0; n < FFT_LEN; n++) {
      double a = -2.0 * PI * k * n / FFT_LEN;
      acc += in[n] * std::complex<double>(std::cos(a), std::sin(a));
    }
    out[k] = acc;
  }
}

int main() {
  const unsigned D = 4094;

  std::complex<double> code_d[FFT_LEN];
  for (unsigned n = 0; n < FFT_LEN; n++) {
    double bit = (std::rand() & 1) ? 0.5 : -0.5;
    code_d[n] = std::complex<double>(bit, 0.0);
  }

  std::complex<double> C[FFT_LEN];
  ref_dft(code_d, C);

  double cmax = 0.0;
  for (unsigned k = 0; k < FFT_LEN; k++) {
    double m = std::abs(C[k]);
    if (m > cmax)
      cmax = m;
  }

  // Arrays for the gold code interface
  fft_data_t code_re_arr[FFT_LEN], code_im_arr[FFT_LEN];
  for (unsigned k = 0; k < FFT_LEN; k++) {
    std::complex<double> cc = std::conj(C[k]) / (cmax * 1.01);
    code_re_arr[k] = (fft_data_t)cc.real();
    code_im_arr[k] = (fft_data_t)cc.imag();
  }

  hls::stream<fft_data_t> stream_iq_re("iq_re");
  hls::stream<fft_data_t> stream_iq_im("iq_im");
  hls::stream<fft_data_t> stream_corr_re("corr_re");
  hls::stream<fft_data_t> stream_corr_im("corr_im");

  const int NUM_FRAMES = 3; // Push multiple frames to test continuous streaming

  // Load ALL frames into the IQ streams back-to-back
  for (int f = 0; f < NUM_FRAMES; f++) {
    for (unsigned n = 0; n < FFT_LEN; n++) {
      unsigned src = (n + FFT_LEN - D) % FFT_LEN;
      stream_iq_re.write((fft_data_t)code_d[src].real());
      stream_iq_im.write((fft_data_t)code_d[src].imag());
    }
  }

  // Run DUT consecutively for each frame
  for (int f = 0; f < NUM_FRAMES; f++) {
    gnss_correlator(stream_iq_re, stream_iq_im, code_re_arr, code_im_arr,
                    stream_corr_re, stream_corr_im);
  }

  // Read magnitudes and verify (Only check the last frame to ensure pipeline
  // clears properly)
  unsigned peak = 0;
  double best = -1.0;

  FILE *fp = fopen("relative_magnitudes.csv", "w");
  if (fp) {
    fprintf(fp, "Lag,Magnitude\n");
  }

  // Drain the output streams. We expect NUM_FRAMES * FFT_LEN outputs.
  for (int f = 0; f < NUM_FRAMES; f++) {
    best = -1.0; // Reset best for each frame
    for (unsigned n = 0; n < FFT_LEN; n++) {
      double re_val = (double)stream_corr_re.read();
      double im_val = (double)stream_corr_im.read();

      double m = std::sqrt(re_val * re_val + im_val * im_val);

      if (m > best) {
        best = m;
        peak = n;
      }

      // Only log the final frame to CSV
      if (fp && f == (NUM_FRAMES - 1)) {
        fprintf(fp, "%u,%.6f\n", n, m);
      }
    }

    printf("Expected peak lag = %u, measured = %u (mag=%.6f)\n", D, peak, best);
  }

  if (fp) {
    fclose(fp);
  }

  if (peak != D) {
    printf("*** TEST FAILED: peak at wrong lag ***\n");
    return 1;
  }

  printf("*** TEST PASSED ***\n");
  return 0;
}
