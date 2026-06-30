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

    # first we create an asymmetric kernel
    kernel = np.array(
        [
            [0, 0, 1],
            [0, 0, 0],
            [0, 0, 0],
        ],
        dtype=float,
    )

    # now we calculate the convolution and correlation using this asymmetric kernel.
    correlation = nd.correlate(img, kernel, mode="wrap")
    convolution = nd.convolve(img, kernel, mode="wrap")

    # plotting the results to understand the effect.
    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap="gray", vmin=0, vmax=1)
    plt.title("original")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(correlation, cmap="gray", vmin=0, vmax=1)
    plt.title("correlation")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(convolution, cmap="gray", vmin=0, vmax=1)
    plt.title("convolution")
    plt.axis("off")

    plt.show()
    diff_abs = np.abs(correlation - convolution)

    plt.figure()
    plt.imshow(diff_abs, cmap="gray")
    plt.colorbar()
    plt.title("|correlation - convolution|")
    plt.show()
