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

    # img.shape = (424, 640, 3). (height, width, colors)
    y, x = img.shape[:2]

    # from spatial coordinates (y, x) to fourier transform sample coordinates (u, v)
    u = np.fft.fftfreq(y)  # shape = (424,)
    v = np.fft.fftfreq(x)  # shape = (640,)

    # since the shape of u and v are only one dimensional we create a 2D meshgrid.
    # so that every (u,v) coordinate has value for u and v.
    # example u: [0, 0.25, -0.5, -0.25] => u = [0, 0.25, -0.5, -0.25
    #                                           0, 0.25, -0.5, -0.25
    #                                           0, 0.25, -0.5, -0.25]
    # and the same process for v as well.
    # it is like creating a matrix from row vector by copying it over each row.

    # shape of both uu and vv is (424, 640) which is same as img.shape without colors
    # means we have value of u and v for each pixel now.
    uu, vv = np.meshgrid(u, v, indexing="ij")

    # now we can create the laplace operator effect on fourier transform.
    # laplace filtering is for edge detection.
    L = -4 * np.pi**2 * (uu**2 + vv**2)

    # we can multiply the laplace operator effect L with the fourier transform of image.
    # it will have the shape (424, 640, 3) which is exactly same as img.shape
    # we have to define axes=(0, 1) which means do fft over height and width.
    # default value is -2, -1 which would be width and color.
    img_ft = np.fft.fft2(img, axes=(0, 1))

    # now we need to inverse the fourier transform
    # we need to use np.newaxis because L is 2D with height and width
    # but img_ft has 3rd dimension for color.
    result = np.fft.ifft2(img_ft * L[:, :, np.newaxis], axes=(0, 1)).real

    # plot the original image and the result.
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap="gray")
    plt.title("Original")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(np.abs(result), cmap="gray")
    plt.title("Laplacian")
    plt.axis("off")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
