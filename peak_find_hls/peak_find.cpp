#include "peak_find.hpp"

static void ingest_data(hls::stream<fp_data> &iq_re,
                        hls::stream<fp_data> &iq_im,
                        fp_data i_raw_buffer[ARRAY_SIZE],
                        fp_data q_raw_buffer[ARRAY_SIZE]) {
INGEST_LOOP:
  for (unsigned n = 0; n < ARRAY_SIZE; n++) {
#pragma HLS PIPELINE II = 1
    i_raw_buffer[n] = iq_re.read();
    q_raw_buffer[n] = iq_im.read();
  }
}

static void calc_magnitude(fp_data i_raw_buffer[ARRAY_SIZE],
                           fp_data q_raw_buffer[ARRAY_SIZE],
                           math_type mag_buffer[ARRAY_SIZE]) {
MAG_LOOP:
  for (unsigned n = 0; n < ARRAY_SIZE; n++) {
#pragma HLS PIPELINE II = 1
    fp_data i_val = i_raw_buffer[n];
    fp_data q_val = q_raw_buffer[n];
    mag_buffer[n] = (i_val * i_val) + (q_val * q_val);
  }
}

static void accumulate_frames(math_type mag_buffer[ARRAY_SIZE],
                              unsigned int run_to,
                              hls::stream<accum_type> &out_stream,
                              hls::stream<bool> &dump_ready_stream) {

  static accum_type internal_accum_buffer[ARRAY_SIZE];
  static unsigned int current_frame = 0;

  bool is_last_frame = (current_frame == (run_to - 1));
  dump_ready_stream.write(is_last_frame);

ACCUM_LOOP:
  for (unsigned i = 0; i < ARRAY_SIZE; i++) {
#pragma HLS PIPELINE II = 1

    accum_type current_val = mag_buffer[i];

    if (current_frame == 0) {
      internal_accum_buffer[i] = current_val;
    } else {
      internal_accum_buffer[i] += current_val;
    }

    if (is_last_frame) {
      out_stream.write(internal_accum_buffer[i]);
    }
  }

  current_frame += 1;
  if (current_frame >= run_to) {
    current_frame = 0;
  }
}

static void find_peak_index(hls::stream<accum_type> &in_stream,
                            hls::stream<bool> &dump_ready_stream,
                            unsigned int &out_peak_index,
                            accum_type &out_peak_value,
                            accum_type &out_noise_mean) {

  // 1. Create static state registers to hold the last valid acquisition.
  // This prevents us from outputting zeros during the accumulating frames.
  static unsigned int current_peak_index = 0;
  static accum_type current_peak_value = 0;
  static accum_type current_noise_mean = 0;

  bool dump_ready = dump_ready_stream.read();

  if (dump_ready) {
    accum_type current_max = 0;
    unsigned int current_index = 0;
    sum_type noise_sum = 0;

  PEAK_LOOP:
    for (unsigned i = 0; i < ARRAY_SIZE; i++) {
#pragma HLS PIPELINE II = 1

      accum_type val = in_stream.read();
      noise_sum += val;

      if (val > current_max) {
        current_max = val;
        current_index = i;
      }
    }

    noise_sum -= current_max;
    accum_type mean_noise = noise_sum >> 12;

    // 2. Update the internal state registers with the new window's data
    current_peak_index = current_index;
    current_peak_value = current_max;
    current_noise_mean = mean_noise;
  }

  // 3. ALWAYS write to the top-level outputs to satisfy the RTL wrapper!
  // On frames 0-3, this safely pushes the old data.
  // On frame 4, it pushes the newly calculated data.
  out_peak_index = current_peak_index;
  out_peak_value = current_peak_value;
  out_noise_mean = current_noise_mean;
}

void peak_find(hls::stream<fp_data> &iq_re, hls::stream<fp_data> &iq_im,
               unsigned int accum_frames, unsigned int &out_peak_index,
               accum_type &out_peak_value, accum_type &out_noise_mean) {

#pragma HLS INTERFACE axis port = iq_re
#pragma HLS INTERFACE axis port = iq_im

#pragma HLS INTERFACE ap_none port = accum_frames
#pragma HLS INTERFACE ap_none port = out_peak_index
#pragma HLS INTERFACE ap_none port = out_peak_value
#pragma HLS INTERFACE ap_none port = out_noise_mean

#pragma HLS INTERFACE ap_ctrl_none port = return

#pragma HLS DATAFLOW

  fp_data i_raw_buffer[ARRAY_SIZE];
  fp_data q_raw_buffer[ARRAY_SIZE];
  math_type mag_buffer[ARRAY_SIZE];

  hls::stream<accum_type> accum_stream("accum_stream");
  hls::stream<bool> dump_ready_stream("dump_ready_stream");

  ingest_data(iq_re, iq_im, i_raw_buffer, q_raw_buffer);
  calc_magnitude(i_raw_buffer, q_raw_buffer, mag_buffer);
  accumulate_frames(mag_buffer, accum_frames, accum_stream, dump_ready_stream);
  find_peak_index(accum_stream, dump_ready_stream, out_peak_index,
                  out_peak_value, out_noise_mean);
}
