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
    # After this, img has shape (height, width).
    img = img[:, :, :3].mean(axis=2)

    # first compute the fourier transform
    # so that image goes from spatial domain to fourier domain.
    F = np.fft.fft2(img)

    # by default numpy puts the zero frequency at top left corner
    # so we need to shift it in the center.
    F_shift = np.fft.fftshift(F)

    # take the absolute value of shifted frequency.
    # frequencies have amplitudes and phase and therefore they are complex values.
    # we want to show only the amplitude
    # and we get the amplitude by taking the abs value.
    amplitudes = np.abs(F_shift)

    # we will get the logarithm of the amplitudes just for visualization purposes.
    # The Fourier magnitude often has a huge dynamic range.
    # The center frequency can be extremely large compared to the others.
    spectrum = np.log(1 + amplitudes)

    plt.figure(figsize=(20, 8))

    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap="gray")
    plt.title("Image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(spectrum, cmap="gray")
    plt.title("Log Fourier spectrum")
    plt.axis("off")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
