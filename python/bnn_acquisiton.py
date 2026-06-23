import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import tensorflow as tf
import larq as lq

from stream_gen import stream_generator

import numpy as np
import matplotlib.pyplot as plt
import string
import random
from scipy.signal import decimate

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
        chunk_duration_s=8184 / sample_rate,
        noise=snr,
        relative_amplitude=wifi_amp,
        phase_offset_samples=phase_offset 
    )

    data_yielder = gen.signal_stream()
    return next(data_yielder)

def train_gen():
    # precalculate values for digitial downsampling
    t = np.arange(8184) / sample_rate
    lo_i = np.cos(2 * np.pi * gnss_fc * t)
    lo_q = -np.sin(2 * np.pi * gnss_fc * t)

    while True:
        # random input string so the bnn doesn't learn on string
        characters = string.ascii_letters + string.digits
        rand_string = ''.join(random.choices(characters, k=15))

        # half the time, we should have no discernable outcome, other half we should
        real_or_fake = random.random()            
        if real_or_fake < 0.5:
            off_freq_or_noise = random.random()
            
            # half the time, have a frequency shifted signal, the other half pure noise
            if off_freq_or_noise < 0.5:
                phase_offset = random.randint(0, 2047)
                freq_offset = random.randint(100, 1000)
                if random.random() > 0.5: freq_offset = -freq_offset
                snr = random.randint(-10, 10)
                wifi_amp = random.randint(-10, 100)
                
                raw_sig = data_stream(rand_string, freq_offset, phase_offset, snr, wifi_amp)
            else:
                raw_sig = np.random.normal(0, 1, 8184)

            detector_target = 0.0
            phase_target = np.zeros(10, dtype=np.float32)

        else:
            # generate real signal
            phase_offset = random.randint(0, 2047)
            freq_offset = 0
            snr = random.randint(-30, 50)
            wifi_amp = random.randint(-100, 10)
            
            raw_sig = data_stream(rand_string, freq_offset, phase_offset, snr, wifi_amp)

            detector_target = 1.0
            decimated_phase_offset = phase_offset // 2
            phase_target = int_to_gray_array(decimated_phase_offset, bits=10).astype(np.float32)

        # mix to IQ
        i_channel = raw_sig * lo_i
        q_channel = raw_sig * lo_q

        i_channel = i_channel[::2]
        q_channel = q_channel[::2]

        i_channel -= np.mean(i_channel)
        q_channel -= np.mean(q_channel)

        # binarize
        i_bin = np.sign(i_channel)
        i_bin[i_bin == 0] = 1.0
        
        q_bin = np.sign(q_channel)
        q_bin[q_bin == 0] = 1.0

        x_out = np.stack((i_bin, q_bin), axis=-1).astype(np.float32)

        yield x_out, {
            "detector": detector_target,
            "phase": phase_target
        }, {
            "detector": 1.0,
            "phase": detector_target
        }

def create_training_dataset(batch_size=32):
    dataset = tf.data.Dataset.from_generator(
        train_gen,
        output_signature=(
            tf.TensorSpec(shape=(4092, 2), dtype=tf.float32),
            {
                "detector": tf.TensorSpec(shape=(), dtype=tf.float32),
                "phase": tf.TensorSpec(shape=(10,), dtype=tf.float32)
            },
            {
                "detector": tf.TensorSpec(shape=(), dtype=tf.float32),
                "phase": tf.TensorSpec(shape=(), dtype=tf.float32)
            }
        )
    )
    
    dataset = dataset.batch(batch_size)
    
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    
    return dataset

bnn_kwargs = dict(
    input_quantizer="ste_sign",
    kernel_quantizer="ste_sign",
    kernel_constraint="weight_clip",
    use_bias=False
)

inputs = tf.keras.layers.Input(shape=(4092, 2))

x = lq.layers.QuantConv1D(filters=32, kernel_size=15, strides=4, padding="same", **bnn_kwargs)(inputs)
x = tf.keras.layers.BatchNormalization(scale=False)(x)

x = lq.layers.QuantConv1D(filters=64, kernel_size=7, strides=4, padding="same", **bnn_kwargs)(x)
x = tf.keras.layers.BatchNormalization(scale=False)(x)

x = lq.layers.QuantConv1D(filters=64, kernel_size=3, strides=4, padding="same", **bnn_kwargs)(x)
x = tf.keras.layers.BatchNormalization(scale=False)(x)

x = tf.keras.layers.Flatten()(x)

x = lq.layers.QuantDense(units=128, **bnn_kwargs)(x)
x = tf.keras.layers.BatchNormalization(scale=False)(x)

# Signal presence neuron
detector_out = tf.keras.layers.Dense(units=1, activation="sigmoid", name="detector")(x)

# Grey code signal out neuron
phase_out = tf.keras.layers.Dense(units=10, activation="sigmoid", name="phase")(x)

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
    metrics=[tf.keras.metrics.BinaryAccuracy()]
)

lq.models.summary(model)

checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath="checkpoints/epoch-{epoch:02d}.weights.h5",
        save_weights_only=True,
        save_best_only=False,
        save_freq="epoch" 
        )

csv_logger = tf.keras.callbacks.CSVLogger('training_log.csv', separator=',', append=False)

train_dataset = create_training_dataset(batch_size=32)

history = model.fit(
    train_dataset,
    steps_per_epoch=100, 
    epochs=100,
    callbacks=[checkpoint_callback, csv_logger]
)

model.save_weights('bnn_saq.weights.h5')
