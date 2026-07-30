#include "gnss_correlator.hpp"

static void fwd_fft(fft_cplx_t in[FFT_LEN], fft_cplx_t out[FFT_LEN]) {
  cfg_t cfg;
  stat_t st;
  cfg.setDir(1);
  cfg.setSch(SCALE_SCHED);
  hls::fft<fft_cfg>(in, out, &st, &cfg);
}
static void inv_fft(fft_cplx_t in[FFT_LEN], fft_cplx_t out[FFT_LEN]) {
  cfg_t cfg;
  stat_t st;
  cfg.setDir(0);
  cfg.setSch(SCALE_SCHED);
  hls::fft<fft_cfg>(in, out, &st, &cfg);
}

void gnss_correlator(fft_data_t iq_re[FFT_LEN], fft_data_t iq_im[FFT_LEN],
                     fft_data_t code_re[FFT_LEN], fft_data_t code_im[FFT_LEN],
                     fft_data_t corr_re[FFT_LEN], fft_data_t corr_im[FFT_LEN],
                     fft_data_t mag_out[FFT_LEN]) {
#pragma HLS INTERFACE ap_vld port = iq_re
#pragma HLS INTERFACE ap_vld port = iq_im
#pragma HLS INTERFACE ap_memory port = code_re
#pragma HLS INTERFACE ap_memory port = code_im
#pragma HLS INTERFACE ap_memory port = corr_re
#pragma HLS INTERFACE ap_memory port = corr_im
#pragma HLS INTERFACE ap_memory port = mag_out
#pragma HLS INTERFACE ap_ctrl_hs port = return

  fft_cplx_t xin[FFT_LEN], Xf[FFT_LEN], prod[FFT_LEN], y[FFT_LEN];

LOAD:
  for (unsigned n = 0; n < FFT_LEN; n++) {
#pragma HLS PIPELINE II = 1
    xin[n] = fft_cplx_t(iq_re[n], iq_im[n]); // stalls until valid high
  }

  fwd_fft(xin, Xf);

CMPLX_MUL:
  for (unsigned k = 0; k < FFT_LEN; k++) {
#pragma HLS PIPELINE II = 1
    fft_cplx_t Xf_val = Xf[k];

    fft_data_t xr = Xf_val.real();
    fft_data_t xi = Xf_val.imag();

    fft_data_t cr = code_re[k], ci = code_im[k];
    ap_fixed<2 * W, 2> pr = xr * cr - xi * ci;
    ap_fixed<2 * W, 2> pi = xr * ci + xi * cr;
    prod[k] = fft_cplx_t((fft_data_t)pr, (fft_data_t)pi);
  }
  inv_fft(prod, y);

STORE:
  for (unsigned n = 0; n < FFT_LEN; n++) {
#pragma HLS PIPELINE II = 1
    fft_cplx_t y_val = y[n];

    fft_data_t re = y_val.real();
    fft_data_t im = y_val.imag();

    corr_re[n] = re;
    corr_im[n] = im;
    mag_out[n] = hls::sqrt((fft_data_t)(re * re + im * im));
  }
}
