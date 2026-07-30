#include "gnss_correlator.hpp"
#include <cmath>
#include <cstdio>
#include <cstdlib>

// Software reference DFT (O(N^2)); forward: X[k] = sum_n x[n] e^{-j2pi kn/N}
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
  const unsigned D = 500; // known circular shift (expected peak lag)

  std::complex<double> code_d[FFT_LEN];
  for (unsigned n = 0; n < FFT_LEN; n++) {
    double bit = (std::rand() & 1) ? 0.5 : -0.5;
    code_d[n] = std::complex<double>(bit, 0.0);
  }

  std::complex<double> C[FFT_LEN];
  ref_dft(code_d, C);

  // find peak magnitude to normalize into [-1,1)
  double cmax = 0.0;
  for (unsigned k = 0; k < FFT_LEN; k++) {
    double m = std::abs(C[k]);
    if (m > cmax)
      cmax = m;
  }

  fft_data_t code_re[FFT_LEN], code_im[FFT_LEN];
  for (unsigned k = 0; k < FFT_LEN; k++) {
    std::complex<double> cc = std::conj(C[k]) / (cmax * 1.01);
    code_re[k] = (fft_data_t)cc.real();
    code_im[k] = (fft_data_t)cc.imag();
  }

  fft_data_t iq_re[FFT_LEN], iq_im[FFT_LEN];
  for (unsigned n = 0; n < FFT_LEN; n++) {
    unsigned src = (n + FFT_LEN - D) % FFT_LEN;
    iq_re[n] = (fft_data_t)code_d[src].real();
    iq_im[n] = (fft_data_t)code_d[src].imag();
  }

  fft_data_t corr_re[FFT_LEN], corr_im[FFT_LEN], mag[FFT_LEN];
  gnss_correlator(iq_re, iq_im, code_re, code_im, corr_re, corr_im, mag);

  unsigned peak = 0;
  double best = -1.0;

  FILE *fp = fopen("relative_magnitudes.csv", "w");
  if (fp) {
    fprintf(fp, "Lag,Magnitude\n");
  }

  for (unsigned n = 0; n < FFT_LEN; n++) {
    double m = (double)mag[n];

    if (m > best) {
      best = m;
      peak = n;
    }

    if (fp) {
      fprintf(fp, "%u,%.6f\n", n, m);
    }
  }

  if (fp) {
    fclose(fp);
  }

  printf("Expected peak lag = %u, measured = %u (mag=%.6f)\n", D, peak, best);

  if (peak != D) {
    printf("*** TEST FAILED: peak at wrong lag ***\n");
    return 1;
  }
  printf("*** TEST PASSED ***\n");
  return 0;
}
