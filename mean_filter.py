import argparse

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as nd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="Path to the input image")
    args = parser.parse_args()

    img = plt.imread(args.image_path) / 255

    # make it gray scale only so it has only width and height dimensions.
    img = img[:, :, :3].mean(axis=2)

    # create the kernel for mean filtering.
    # the kernel has the same value for each pixel in mean filtering.
    kernel = np.ones((13, 13))

    # normalize the kernel so divide every pixel with the sum of the kernel values.
    # this makes the sum of kernel values 1
    # and avoids highering or lowering the brigthness after filtering.
    kernel = kernel / kernel.sum()

    # we can make a convolution in spatial domain or multiplication in fourier domain.
    result_mean = nd.convolve(img, kernel, mode="wrap")

    # create the kernel for gauss filtering.
    sigma = 5.0
    radius = int(np.ceil(4 * sigma))

    # create the row of the kernel. it will just go from -8 to 8.
    # it will describe the position of the pixel relative to the center.
    x = np.arange(-radius, radius + 1)

    # make a matrix out of this row in 2D because the image is 2D as well.
    xx, yy = np.meshgrid(x, x)

    # apply each value of this 2D matrix in the gauss distribution to create kernel.
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))

    # normalize the kernel.
    kernel = kernel / kernel.sum()

    # we can make a convolution in spatial domain or multiplication in fourier domain.
    result_gauss = nd.convolve(img, kernel, mode="wrap")

    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap="gray", vmin=0, vmax=1)
    plt.title("original")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(result_mean, cmap="gray", vmin=0, vmax=1)
    plt.title("mean filtered")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(result_gauss, cmap="gray", vmin=0, vmax=1)
    plt.title("gauss filtered")
    plt.axis("off")

    plt.show()
