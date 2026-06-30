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

    # make it gray scale only so it has only width and height dimensions.
    img = img[:, :, :3].mean(axis=2)

    img_8bit = (img * 255).astype(np.uint8)
    img_4bit = np.floor(img * 16) / 15
    img_2bit = np.floor(img * 4) / 3
    img_1bit = img > 0.5

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 4, 1)
    plt.imshow(img_8bit, cmap="gray")
    plt.title("Original")
    plt.axis("off")

    plt.subplot(1, 4, 2)
    plt.imshow(img_4bit, cmap="gray")
    plt.title("4-bit")
    plt.axis("off")

    plt.subplot(1, 4, 3)
    plt.imshow(img_2bit, cmap="gray")
    plt.title("2-bit")
    plt.axis("off")

    plt.subplot(1, 4, 4)
    plt.imshow(img_1bit, cmap="gray")
    plt.title("1-bit")
    plt.axis("off")

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
