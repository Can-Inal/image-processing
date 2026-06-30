import argparse

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="Path to the input image")
    args = parser.parse_args()

    img = plt.imread(args.image_path) / 255

    # Convert RGB image to grayscale by averaging the red, green, and blue channels.
    img = img[:, :, :3].mean(axis=2)

    # Get image height and width.
    h, w = img.shape

    # Now convert the image to fourier domain.
    img_ft = np.fft.fft2(img, axes=(0, 1))

    # Shift the zero frequency into the center.
    img_ft_shifted = np.fft.fftshift(img_ft, axes=(0, 1))

    # Create the zero-centered x and y coordinates for fourier domain.
    x = np.arange(w) - w // 2
    y = np.arange(h) - h // 2

    # Create the meshgrid so that every pixel in fourier domain has a coordinate value.
    yy, xx = np.meshgrid(y, x, indexing="ij")

    # Calculate the distance between each coordinate to the center.
    r = np.sqrt(xx**2 + yy**2)

    # Define the low and high frequency cutoffs.
    # The frequencies between 30 and 60 will stop, and all other frequencies will pass.
    r_low = 30.0
    r_high = 60.0

    # Create the mask.
    band_stop_mask = (r <= r_low) | (r >= r_high)

    # Apply the mask in img_ft_shifted by multiplying them.
    img_ft_shifted_band_stop = img_ft_shifted * band_stop_mask

    # Re-shift it back to the default.
    img_ft_band_stop = np.fft.ifftshift(img_ft_shifted_band_stop, axes=(0, 1))

    # Transform it back to the spatial domain.
    img_band_stop = np.fft.ifft2(img_ft_band_stop, axes=(0, 1)).real

    # Plot original and band pass image.
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap="gray")
    plt.title("original")

    plt.subplot(1, 2, 2)
    plt.imshow(img_band_stop, cmap="gray")
    plt.title("band stop image")

    plt.show()
