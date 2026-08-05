#ifndef PEAK_FIND_HPP
#define PEAK_FIND_HPP

#include "ap_fixed.h"
#include "hls_math.h"
#include "hls_stream.h"

static const int W = 16;
static const int ARRAY_SIZE = 4096;

typedef ap_fixed<W, 1> fp_data;
typedef ap_fixed<W * 2 + 1, 3> math_type;
typedef ap_fixed<W * 2 + 4, 8> accum_type;

typedef ap_fixed<accum_type::width + 12, accum_type::iwidth + 12> sum_type;

void peak_find(hls::stream<fp_data> &iq_re, hls::stream<fp_data> &iq_im,
               unsigned int accum_frames, unsigned int &out_peak_index,
               accum_type &out_peak_value, accum_type &out_noise_mean);

#endif
