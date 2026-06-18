import numpy as np
import plotly.graph_objects as go
from collections import defaultdict

def plot_3d_correlator_map(outputs):
    """
    outputs: list of tuples -> [(scan_freq_1, corr_output_1), (scan_freq_2, corr_output_2), ...]
    """
    
    # 1. Group correlator outputs by frequency
    freq_dict = defaultdict(list)
    
    for freq, corr_array in outputs:
        intensity = np.abs(corr_array)
        freq_dict[freq].append(intensity)

    # 2. Average the results for non-unique frequencies
    unique_freqs = sorted(freq_dict.keys())
    avg_intensities = []

    for f in unique_freqs:
        avg_array = np.mean(freq_dict[f], axis=0)
        avg_intensities.append(avg_array)

    Z = np.array(avg_intensities)
    X = unique_freqs
    Y = np.arange(Z.shape[1])

    # 3. Plot using Plotly
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])

    fig.update_layout(
        title='3D Frequency-Delay Map',
        scene=dict(
            xaxis_title='Scan Frequency (Doppler Shift)',
            yaxis_title='Correlator Index (Delay/Range Bin)',
            zaxis_title='Intensity (Magnitude)'
        ),
        autosize=False,
        width=1000, 
        height=800,
        margin=dict(l=65, r=50, b=65, t=90)
    )

    fig.show()
