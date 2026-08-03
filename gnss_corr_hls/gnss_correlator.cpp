#include "gnss_correlator.hpp"

static void ingest_data(hls::stream<fft_data_t> &iq_re,
                        hls::stream<fft_data_t> &iq_im,
                        fft_cplx_t raw_buffer[FFT_LEN]) {
INGEST_LOOP:
  for (unsigned n = 0; n < FFT_LEN; n++) {
#pragma HLS PIPELINE II = 1
    raw_buffer[n] = fft_cplx_t(iq_re.read(), iq_im.read());
  }
}

static void remove_dc(fft_cplx_t raw_buffer[FFT_LEN],
                      fft_cplx_t dc_buffer[FFT_LEN]) {
  static fft_data_t prev_mean_re = 0;
  static fft_data_t prev_mean_im = 0;

  float current_sum_re = 0.0f;
  float current_sum_im = 0.0f;

DC_LOOP:
  for (unsigned n = 0; n < FFT_LEN; n++) {
#pragma HLS PIPELINE II = 1
    fft_cplx_t in_val = raw_buffer[n];
    fft_data_t in_re = in_val.real();
    fft_data_t in_im = in_val.imag();

    current_sum_re += (float)in_re;
    current_sum_im += (float)in_im;

    fft_data_t out_re = in_re - prev_mean_re;
    fft_data_t out_im = in_im - prev_mean_im;

    dc_buffer[n] = fft_cplx_t(out_re, out_im);
  }

  prev_mean_re = (fft_data_t)(current_sum_re / FFT_LEN);
  prev_mean_im = (fft_data_t)(current_sum_im / FFT_LEN);
}

static void fwd_fft(fft_cplx_t in[FFT_LEN], fft_cplx_t out[FFT_LEN]) {
  cfg_t cfg;
  stat_t st;
  cfg.setDir(1);
  cfg.setSch(SCALE_SCHED);
  hls::fft<fft_cfg>(in, out, &st, &cfg);
  volatile bool dummy = st.getOvflo();
}

static void cmplx_mul(fft_cplx_t Xf[FFT_LEN], fft_data_t code_re[FFT_LEN],
                      fft_data_t code_im[FFT_LEN], fft_cplx_t prod[FFT_LEN]) {
CMPLX_MUL:
  for (unsigned k = 0; k < FFT_LEN; k++) {
#pragma HLS PIPELINE II = 1
    fft_cplx_t Xf_val = Xf[k];
    fft_data_t xr = Xf_val.real();
    fft_data_t xi = Xf_val.imag();

    fft_data_t cr = code_re[k];
    fft_data_t ci = code_im[k];

    ap_fixed<2 * W, 2> pr = xr * cr - xi * ci;
    ap_fixed<2 * W, 2> pi = xr * ci + xi * cr;

    prod[k] = fft_cplx_t((fft_data_t)pr, (fft_data_t)pi);
  }
}

static void inv_fft(fft_cplx_t in[FFT_LEN], fft_cplx_t out[FFT_LEN]) {
  cfg_t cfg;
  stat_t st;
  cfg.setDir(0);
  cfg.setSch(SCALE_SCHED);
  hls::fft<fft_cfg>(in, out, &st, &cfg);
  volatile bool dummy = st.getOvflo();
}

static void store_output(fft_cplx_t y[FFT_LEN],
                         hls::stream<fft_data_t> &corr_re,
                         hls::stream<fft_data_t> &corr_im) {
STORE:
  for (unsigned n = 0; n < FFT_LEN; n++) {
#pragma HLS PIPELINE II = 1
    fft_cplx_t y_val = y[n];
    corr_re.write(y_val.real());
    corr_im.write(y_val.imag());
  }
}

void gnss_correlator(hls::stream<fft_data_t> &iq_re,
                     hls::stream<fft_data_t> &iq_im,
                     fft_data_t code_re[FFT_LEN], fft_data_t code_im[FFT_LEN],
                     hls::stream<fft_data_t> &corr_re,
                     hls::stream<fft_data_t> &corr_im) {

#pragma HLS INTERFACE axis port = iq_re
#pragma HLS INTERFACE axis port = iq_im
#pragma HLS INTERFACE axis port = corr_re
#pragma HLS INTERFACE axis port = corr_im

#pragma HLS INTERFACE ap_memory port = code_re storage_type = ram_1p
#pragma HLS INTERFACE ap_memory port = code_im storage_type = ram_1p
#pragma HLS INTERFACE ap_ctrl_none port = return

#pragma HLS DATAFLOW

  fft_cplx_t raw_buffer[FFT_LEN];
  fft_cplx_t dc_buffer[FFT_LEN];

  fft_cplx_t Xf[FFT_LEN], prod[FFT_LEN], y[FFT_LEN];

#pragma HLS STREAM variable = Xf depth = FFT_LEN
#pragma HLS STREAM variable = prod depth = FFT_LEN
#pragma HLS STREAM variable = y depth = FFT_LEN

  ingest_data(iq_re, iq_im, raw_buffer);
  remove_dc(raw_buffer, dc_buffer);
  fwd_fft(dc_buffer, Xf);
  cmplx_mul(Xf, code_re, code_im, prod);
  inv_fft(prod, y);
  store_output(y, corr_re, corr_im);
}
