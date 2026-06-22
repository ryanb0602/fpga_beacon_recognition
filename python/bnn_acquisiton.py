import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import tensorflow as tf
import larq as lq

from stream_gen import stream_generator

import numpy as np
import matplotlib.pyplot as plt
import string
import random

gnss_fc = 2.046e6
sample_rate = 10e6

#convert into to gray code
def int_to_gray_array(n, bits=11):
    gray = n ^ (n >> 1)
    return np.array([float(x) for x in format(gray, f'0{bits}b')])

def data_stream(rand_string, freq_offset, phase_offset, snr, wifi_amp):

    gen = stream_generator(
        gnss_string=rand_string,
        gnss_fc=gnss_fc + freq_offset,                   # GNSS at 2x chip rate
        gnss_transmission_speed=50,
        wifi_fc=3e6,                   # WiFi about 1Mhz above gnss
        stream_sample_rate=sample_rate,       # 10 MHz sample rate
        chunk_duration_s=4092 / sample_rate,
        noise=snr,
        relative_amplitude=wifi_amp,
        phase_offset_samples=phase_offset 
    )

    data_yielder = gen.signal_stream()
    return next(data_yielder)

def train_gen(batch_size=32):
    # precalculate values for digitial downsampling
    t = np.arange(4092) / sample_rate
    lo_i = np.cos(2 * np.pi * gnss_fc * t)
    lo_q = -np.sin(2 * np.pi * gnss_fc * t)

    while True:
        batch_x = np.zeros((batch_size, 4092, 2), dtype=np.float32)
        batch_detector = np.zeros((batch_size, 1), dtype=np.float32)
        batch_phase = np.zeros((batch_size, 11), dtype=np.float32)
        
        #generate for num of batches
        for i in range(batch_size):
            #random input string so the bnn doesn't learn on string
            characters = string.ascii_letters + string.digits
            rand_string = ''.join(random.choices(characters, k=15))

            #half the time, we should have no discernable outcome, other half we should
            real_or_fake = random.random()            
            if real_or_fake < 0.5:
                off_freq_or_noise = random.random()
               
                #half the time, have a frequency shifted signal, the other half pure noise
                if off_freq_or_noise < 0.5:
                    phase_offset = random.randint(0, 2047)
                    freq_offset = random.randint(100, 1000)
                    if random.random() > 0.5: freq_offset = -freq_offset
                    snr = random.randint(-10, 10)
                    wifi_amp = random.randint(-10, 10)
                    
                    raw_sig = data_stream(rand_string, freq_offset, phase_offset, snr, wifi_amp)
                else:
                    raw_sig = np.random.normal(0, 1, 4092)

                batch_detector[i] = 0.0
                batch_phase[i] = np.zeros(11)
            else:
                #generate real signal
                phase_offset = random.randint(0, 2047)
                freq_offset = 0
                snr = random.randint(-20, 10)
                wifi_amp = random.randint(-20, 10)
                
                raw_sig = data_stream(rand_string, freq_offset, phase_offset, snr, wifi_amp)

                batch_detector[i] = 1.0
                batch_phase[i] = int_to_gray_array(phase_offset, bits=11)

            #mix to IQ and binarize
            i_channel = raw_sig * lo_i
            q_channel = raw_sig * lo_q

            i_channel -= np.mean(i_channel)
            q_channel -= np.mean(q_channel)

            i_bin = np.sign(i_channel)
            i_bin[i_bin == 0] = 1.0
            
            q_bin = np.sign(q_channel)
            q_bin[q_bin == 0] = 1.0

            batch_x[i, :, 0] = i_bin
            batch_x[i, :, 1] = q_bin

        yield (batch_x, {
            "detector": batch_detector,
            "phase": batch_phase
        })

bnn_kwargs = dict(
    input_quantizer="ste_sign",
    kernel_quantizer="ste_sign",
    kernel_constraint="weight_clip",
    use_bias=False
)

inputs = tf.keras.layers.Input(shape=(4092, 2))

x = lq.layers.QuantConv1D(filters=32, kernel_size=15, padding="same", **bnn_kwargs)(inputs)
x = tf.keras.layers.BatchNormalization(scale=False)(x)
x = tf.keras.layers.MaxPooling1D(pool_size=4)(x)

x = lq.layers.QuantConv1D(filters=64, kernel_size=7, padding="same", **bnn_kwargs)(x)
x = tf.keras.layers.BatchNormalization(scale=False)(x)
x = tf.keras.layers.MaxPooling1D(pool_size=4)(x)

x = tf.keras.layers.Flatten()(x)

x = lq.layers.QuantDense(units=128, **bnn_kwargs)(x)
x = tf.keras.layers.BatchNormalization(scale=False)(x)

#Signal presence neuron
detector_out = tf.keras.layers.Dense(units=1, activation="sigmoid", name="detector")(x)

#Grey code signal out neuron
phase_out = tf.keras.layers.Dense(units=11, activation="sigmoid", name="phase")(x)

model = tf.keras.Model(inputs=inputs, outputs=[detector_out, phase_out])

model.compile(
    optimizer="adam",
    loss={
        "detector": "binary_crossentropy",
        "phase": "binary_crossentropy"
    },
    loss_weights={
        "detector": 1.0,
        "phase": 1.0
    },
    metrics=["accuracy"]
)

lq.models.summary(model)

history = model.fit(
    train_gen(batch_size=32),
    steps_per_epoch=100, 
    epochs=100
)

model.save_weights('bnn_saq.weights.h5')
