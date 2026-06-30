import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as nd

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

    # using scipy library it is one line code.
    img_filtered = nd.gaussian_filter(input=img, sigma=(10, 10, 0))

    # now doing it by ourself.
    # first we need to create the kernel.
    # it is np.exp(-(x**2 + y**2)/(2*sigma**2))
    # without normalization 1/(2*pi*sigma**2)
    # because we will do the normalization by kernel / kernel.sum()
    sigma = 10.0
    radius = int(np.ceil(4 * sigma))

    # need to add 1 because stop is exclusive
    # so it will stop before the radius otherwise.
    x = np.arange(-radius, radius + 1)

    # now just like wit the laplace filter we need to create 2d meshgrid
    # but this time both width and height will have same values.
    xx, yy = np.meshgrid(x, x, indexing="xy")

    # now we have the x and y ranges (xx, yy) for the kernel in 2d spatial domain.
    # we can use them to create the not normalized gaussian distribution.
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))

    # now we will normalize the distribution
    kernel = kernel / kernel.sum()

    # lets handle border issue
    pad = kernel.shape[0] // 2
    img_pad = np.pad(
        array=img, pad_width=((pad, pad), (pad, pad), (0, 0)), mode="reflect"
    )

    # now we start with convolution in spatial domain
    h, w, c = img.shape
    hp, wp, cp = img_pad.shape
    kh, kw = kernel.shape

    result_spatial = np.zeros_like(img)

    for y in range(h):
        for x in range(w):
            # take the corresponding part of the padded image for convolution
            patch = img_pad[y : y + kh, x : x + kw, :]
            result_spatial[y, x] = np.sum(patch * kernel[..., np.newaxis], axis=(0, 1))

    # now we will do the same but in fourier domain as multiplication.
    # since we have kernel pad we use the dimensions of image pad.
    kernel_pad = np.zeros((hp, wp))

    # set the kernel in the center of kernel pad
    kernel_pad[
        hp // 2 - kh // 2 : hp // 2 + kh // 2 + 1,
        wp // 2 - kw // 2 : wp // 2 + kw // 2 + 1,
    ] = kernel

    # shift the kernel center to the top left corner for the fft before fft.
    kernel_pad = np.fft.ifftshift(kernel_pad)

    # after shifting the kernel we can get ffts both for kernel and image.
    kernel_ft = np.fft.fft2(kernel_pad)
    img_ft = np.fft.fft2(img_pad, axes=(0, 1))

    # convolution in spatial domain is multiplication in fourier domain.
    result_fourier = np.fft.ifft2(img_ft * kernel_ft[..., np.newaxis], axes=(0, 1)).real

    # cut off the padding
    # because we use padded image and kernel to create result_fourier.
    result_fourier = result_fourier[pad : pad + h, pad : pad + w, :]

    plt.subplot(1, 3, 1)
    plt.imshow(img_filtered, cmap="gray")
    plt.title("Scipy")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(result_spatial, cmap="gray")
    plt.title("Spatial")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(result_fourier, cmap="gray")
    plt.title("Fourier")
    plt.axis("off")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
