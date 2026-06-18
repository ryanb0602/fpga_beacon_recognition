import os
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def stitch_images():
    image_dir = '.'  # Current directory. Change if your images are elsewhere.
    
    # 1. Regex pattern to extract SNR (Y) and WiFi (X) values
    # It looks for optional minus signs (-?) followed by digits (\d+)
    pattern = re.compile(r'(-?\d+)snr_(-?\d+)wifi_correlator_map\.png')

    data = []
    
    # 2. Parse filenames and extract data
    for filename in os.listdir(image_dir):
        match = pattern.match(filename)
        if match:
            snr_val = int(match.group(1))
            wifi_val = int(match.group(2))
            data.append({
                'filename': os.path.join(image_dir, filename), 
                'snr': snr_val, 
                'wifi': wifi_val
            })

    if not data:
        print("No matching images found in the directory.")
        return

    # 3. Determine the grid size by finding unique X and Y values
    # SNR is usually plotted with highest at the top, so we reverse sort Y
    unique_snr = sorted(list(set([d['snr'] for d in data])), reverse=True)
    # WiFi sorted lowest to highest for X
    unique_wifi = sorted(list(set([d['wifi'] for d in data])))

    # Create mapping from value to grid index
    snr_to_row = {val: i for i, val in enumerate(unique_snr)}
    wifi_to_col = {val: i for i, val in enumerate(unique_wifi)}

    nrows = len(unique_snr)
    ncols = len(unique_wifi)

    # 4. Set up the Matplotlib figure
    # squeeze=False ensures 'axes' is always a 2D array, even if it's a 1x1 grid
    # gridspec_kw removes the whitespace between images to truly "stitch" them
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, 
                             figsize=(ncols * 3, nrows * 3), 
                             gridspec_kw={'wspace': 0, 'hspace': 0},
                             squeeze=False)

    # Turn off axes for all subplots initially (in case some grid spots are missing images)
    for ax in axes.flat:
        ax.axis('off')

    # 5. Populate the grid
    for item in data:
        row = snr_to_row[item['snr']]
        col = wifi_to_col[item['wifi']]
        ax = axes[row, col]

        # Load and display the image
        img = mpimg.imread(item['filename'])
        ax.imshow(img)
        
        # Turn the axis back on so we can see the borders, but remove tick marks
        ax.axis('on')
        ax.set_xticks([])
        ax.set_yticks([])

        # Label the outer edges to create the master axis
        if col == 0:
            ax.set_ylabel(f'{item["snr"]} SNR', fontsize=12, fontweight='bold')
        if row == nrows - 1:
            ax.set_xlabel(f'{item["wifi"]} WiFi', fontsize=12, fontweight='bold')

    # 6. Add master titles and save
    fig.suptitle('Correlator Map Matrix: SNR vs WiFi', fontsize=16, fontweight='bold', y=1)
    plt.tight_layout()
    
    output_filename = 'stitched_correlator_matrix.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Success! Image saved as {output_filename}")
    
    # Opens the window to view the result immediately
    plt.show()

if __name__ == '__main__':
    stitch_images()
