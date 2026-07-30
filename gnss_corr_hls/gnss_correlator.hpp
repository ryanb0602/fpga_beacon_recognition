#ifndef GNSS_CORRELATOR_HPP
#define GNSS_CORRELATOR_HPP

#include "ap_fixed.h"
#include "hls_fft.h"
#include "hls_math.h"
#include <complex>

static const unsigned FFT_LEN = 1024;
static const unsigned FFT_NFFT = 10;

static const int W = 24;

typedef ap_fixed<W, 1> fft_data_t; // range [-1, 1)
typedef std::complex<fft_data_t> fft_cplx_t;

struct fft_cfg : hls::ip_fft::params_t {
  static const unsigned ordering_opt = hls::ip_fft::natural_order;
  static const unsigned max_nfft = FFT_NFFT;
  static const unsigned input_width = W;
  static const unsigned output_width = W;
  static const unsigned scaling_opt = hls::ip_fft::scaled;
  static const unsigned phase_factor_width = 24;
};
typedef hls::ip_fft::config_t<fft_cfg> cfg_t;
typedef hls::ip_fft::status_t<fft_cfg> stat_t;

static const unsigned SCALE_SCHED = 0x55556;
void gnss_correlator(fft_data_t iq_re[FFT_LEN], fft_data_t iq_im[FFT_LEN],
                     fft_data_t code_re[FFT_LEN], fft_data_t code_im[FFT_LEN],
                     fft_data_t corr_re[FFT_LEN], fft_data_t corr_im[FFT_LEN],
                     fft_data_t mag_out[FFT_LEN]);

#endif
