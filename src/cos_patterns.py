import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        help="Path where the output figure should be saved",
    )
    args = parser.parse_args()

    # define the image size.
    h = 424
    w = 640

    # create pixel positions for y and x direction.
    y = np.arange(h)
    x = np.arange(w)

    # since x and y are one dimensional we need to create a 2D grid.
    # xx contains the x coordinate for every pixel.
    # yy contains the y coordinate for every pixel.
    xx, yy = np.meshgrid(x, y)

    # how many bright/dark waves we want across the image width.
    cycles = 10

    # cycles per pixel in x direction.
    freq = cycles / w

    # create a synthetic cosine pattern image.
    # since we use xx here, the brightness changes in x direction.
    # that means the image will have vertical stripes.
    img = np.cos(2 * np.pi * freq * xx)

    # apply 2D fft to move the image from spatial domain to frequency domain.
    F = np.fft.fft2(img)

    # move the zero frequency to the center for visualization.
    F_shift = np.fft.fftshift(F)

    # calculate the amplitudes of the complex frequency values.
    amplitudes = np.abs(F_shift)

    # take log for better visualization
    # because the amplitudes can have very large values.
    spectrum = np.log(1 + amplitudes)

    # plot the synthetic image and its fourier spectrum.
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap="gray")
    plt.title("cosine image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(spectrum, cmap="gray")
    plt.title("spectrum")
    plt.axis("off")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
