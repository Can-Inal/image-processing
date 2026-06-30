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
    fig1 = plt.figure()

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

    diff_abs = np.abs(correlation - convolution)

    fig2 = plt.figure()
    plt.imshow(diff_abs, cmap="gray")
    plt.colorbar()
    plt.title("|correlation - convolution|")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        suffix = output_path.suffix if output_path.suffix else ".png"
        main_output_path = output_path.with_suffix(suffix)
        diff_output_path = output_path.with_name(f"{output_path.stem}_diff{suffix}")

        fig1.savefig(main_output_path, dpi=300, bbox_inches="tight")
        fig2.savefig(diff_output_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
