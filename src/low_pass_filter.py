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

    # Transform the image to Fourier domain.
    img_ft = np.fft.fft2(img)

    # Shift zero frequency to the center.
    img_ft_shift = np.fft.fftshift(img_ft)

    # Create coordinates centered at the middle of the spectrum.
    y = np.arange(h) - h // 2
    x = np.arange(w) - w // 2
    xx, yy = np.meshgrid(x, y)

    # Calculate distance of every frequency position from the center.
    r = np.sqrt(xx**2 + yy**2)

    # Choose cutoff radius.
    cutoff = 20

    # Low-pass keeps frequencies close to the center.
    lowpass_mask = r <= cutoff

    # Apply low-pass mask in Fourier domain.
    img_ft_low = img_ft_shift * lowpass_mask

    # Move zero frequency back and transform to spatial domain.
    img_low_pass = np.fft.ifft2(np.fft.ifftshift(img_ft_low)).real

    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap="gray", vmin=0, vmax=1)
    plt.title("original")
    plt.axis("off")

    # low pass filter does not need np.abs since it contains the frequencies near zero.
    # which are mostly already in an image range of [0, 1]
    plt.subplot(1, 3, 2)
    plt.imshow(img_low_pass, cmap="gray", vmin=0, vmax=1)
    plt.title("low pass")
    plt.axis("off")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
