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

    # After this, img has shape (height, width).
    img = img[:, :, :3].mean(axis=2)

    # A simple discrete first derivative in x-direction can be approximated by:
    #     f[x + 1] - f[x - 1]
    # This measures how strongly the image intensity changes from left to right.
    #
    # Sobel extends this idea by combining:
    #     [-1, 0, 1]   -> derivative in x-direction
    #     [1, 2, 1]^T  -> smoothing in y-direction
    #
    # Therefore, Sobel x detects vertical edges.
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)

    # Sobel y works analogously:
    #     [-1, 0, 1]^T -> derivative in y-direction
    #     [1, 2, 1]    -> smoothing in x-direction
    #
    # Therefore, Sobel y detects horizontal edges.
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)

    # Apply the Sobel kernels by convolution.
    # gx contains the horizontal intensity-change response,
    # so it is strong at vertical edges.
    #
    # gy contains the vertical intensity-change response,
    # so it is strong at horizontal edges.
    gx = nd.convolve(img, sobel_x, mode="wrap")
    gy = nd.convolve(img, sobel_y, mode="wrap")

    # Combine the x- and y-derivative responses into one edge-strength image.
    # This is the gradient magnitude:
    #     |grad f| = sqrt(gx^2 + gy^2)
    #
    # It is large wherever the image changes strongly in any direction.
    grad_mag = np.sqrt(gx**2 + gy**2)

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(grad_mag, cmap="gray")
    plt.title("Sobel magnitude")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(gx, cmap="gray")
    plt.title("x-derivative: vertical edges")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(gy, cmap="gray")
    plt.title("y-derivative: horizontal edges")
    plt.axis("off")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
