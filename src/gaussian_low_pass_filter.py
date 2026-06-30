import argparse

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="Path to the input image")
    args = parser.parse_args()

    img = plt.imread(args.image_path) / 255

    # Convert RGB image to grayscale by averaging the red, green, and blue channels.
    img = img[:, :, :3].mean(axis=2)

    # Get image height and width.
    h, w = img.shape

    # Get fourier domain of image.
    img_ft = np.fft.fft2(img, axes=(0, 1))

    # Shift fourier to the center.
    img_ft_shifted = np.fft.fftshift(img_ft, axes=(0, 1))

    # create x and y coordinates for fourier domain where zero is in the center.
    x = np.arange(w) - w // 2
    y = np.arange(h) - h // 2

    # create the xx, yy meshgrid so that each pixel has both x and y coordinates.
    yy, xx = np.meshgrid(y, x, indexing="ij")

    # calculate the distance from each pixel to the center of the fourier domain.
    r = np.sqrt(xx**2 + yy**2)

    # create the gaussian mask for low pass.
    # for gaussian filter the cutoff is the sigma value.
    sigma = 40.0
    gaussian_mask = np.exp(-(r**2) / (2 * sigma**2))

    # apply the gaussian mask by multiplying it with the img_ft_shifted.
    img_ft_shifted_gaussian = img_ft_shifted * gaussian_mask

    # now convert it back to default before going to the spatial domain.
    img_ft_gaussian = np.fft.ifftshift(img_ft_shifted_gaussian, axes=(0, 1))

    # now we can go back to the spatial domain.
    img_gaussian = np.fft.ifft2(img_ft_gaussian, axes=(0, 1)).real

    # plot the original image and gaussian low pass filter image.
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap="gray")
    plt.title("original")

    plt.subplot(1, 2, 2)
    plt.imshow(img_gaussian, cmap="gray")
    plt.title("gaussian low pass filter")

    plt.show()
