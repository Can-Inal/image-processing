import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="Path to the input image")
    parser.add_argument(
        "-o",
        "--output",
        help="Path where the output figure should be saved",
    )
    args = parser.parse_args()

    img = plt.imread(args.image_path) / 255

    # Convert RGB image to grayscale by averaging the red, green, and blue channels.
    img = img[:, :, :3].mean(axis=2)

    # Get image height and width.
    h, w = img.shape

    # Get fourier domain of the image.
    img_ft = np.fft.fft2(img, axes=(0, 1))

    # shift zero frequency to the center.
    img_ft_shifted = np.fft.fftshift(img_ft)

    # create 0 centered coordinates for the shifted fourier transform of the image.
    y = np.arange(h) - h // 2
    x = np.arange(w) - w // 2

    # these x and y are 1D. we need to make a meshgrid.
    yy, xx = np.meshgrid(y, x, indexing="ij")

    # calculate the distance of the coordinates from the center.
    r = np.sqrt(xx**2 + yy**2)

    # create the cutoff for high pass filter.
    cutoff = 30

    # create the high pass mask based on the cutoff.
    high_pass_mask = r > cutoff

    # calculate the frequencies which will be discarded or not.
    img_ft_high_pass_shifted = img_ft_shifted * high_pass_mask

    # shift zero frequency to top left which is where it should be by default.
    img_ft_high_pass = np.fft.ifftshift(img_ft_high_pass_shifted, axes=(0, 1))

    # from fourier domain go back to spatial domain.
    img_high_pass = np.fft.ifft2(img_ft_high_pass, axes=(0, 1)).real

    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap="gray")
    plt.title("original")
    plt.axis("off")

    # to plot high pass filtered image we need to take abs value.
    # it contains small positive and negative values.
    plt.subplot(1, 2, 2)
    img_high_pass_abs = np.abs(img_high_pass)
    plt.imshow(
        img_high_pass_abs,
        cmap="gray",
        vmin=0,
        vmax=np.percentile(img_high_pass_abs, 99),
    )
    plt.title("high pass")
    plt.axis("off")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
