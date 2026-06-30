# Image Processing Experiments

Small Python scripts for learning and experimenting with image processing concepts.

This repository covers spatial-domain filtering, Fourier-domain filtering, edge detection, sampling, quantization, and synthetic frequency patterns.

The repository does not include an input image. To run the image-based scripts, use your own image file and pass its path as a command-line argument.

## Examples

### Fourier Spectrum

```bash
python src/fourier_spectrum.py path/to/your_image.jpg -o assets/fourier_spectrum.png
```

![Fourier spectrum](assets/fourier_spectrum.png)

This example computes the Fourier transform of the image and displays the magnitude spectrum. The bright center represents low frequencies, which correspond to large smooth structures in the image. Brighter points or lines farther away from the center represent stronger high-frequency components, such as edges, texture, and repeated patterns.

### Sobel Edge Detection

```bash
python src/sobel_filter.py path/to/your_image.jpg -o assets/sobel_filter.png
```

![Sobel filter](assets/sobel_filter.png)

The Sobel filter estimates image gradients. The x-derivative image highlights vertical edges because it responds to left-right intensity changes. The y-derivative image highlights horizontal edges because it responds to up-down intensity changes. The magnitude image combines both directions and shows the overall edge strength.

### Low-Pass and High-Pass Filtering

```bash
python src/low_pass_filter.py path/to/your_image.jpg -o assets/low_pass_filter.png
python src/high_pass_filter.py path/to/your_image.jpg -o assets/high_pass_filter.png
```

![Low-pass filter](assets/low_pass_filter.png)

The low-pass result keeps frequencies close to the center of the Fourier spectrum and removes higher frequencies. This preserves broad, smooth image structures while reducing sharp details and texture, so the output looks blurred.

![High-pass filter](assets/high_pass_filter.png)

The high-pass result removes low frequencies near the center and keeps frequencies farther away from the center. This suppresses smooth regions and emphasizes rapid intensity changes, so edges and fine details become more visible.

### Gaussian Filtering

```bash
python src/gaussian_filter.py path/to/your_image.jpg -o assets/gaussian_filter.png
```

![Gaussian filter](assets/gaussian_filter.png)

This example compares Gaussian smoothing methods. Gaussian filtering blurs the image by averaging nearby pixels with weights that decrease with distance from the center. The result removes small details and noise while preserving the general structure of the image.

### Gaussian Low-Pass Filtering

```bash
python src/gaussian_low_pass_filter.py path/to/your_image.jpg -o assets/gaussian_low_pass_filter.png
```

![Gaussian low-pass filter](assets/gaussian_low_pass_filter.png)

This example applies a Gaussian low-pass mask in the Fourier domain. Unlike an ideal low-pass filter with a sharp cutoff, the Gaussian mask decreases smoothly as the distance from the center increases. This creates smoother blur and reduces strong ringing artifacts.

### Band-Pass and Band-Stop Filtering

```bash
python src/band_pass_filter.py path/to/your_image.jpg -o assets/band_pass.png
python src/band_stop_filter.py path/to/your_image.jpg -o assets/band_stop.png
```

![Band-pass filter](assets/band_pass.png)

The band-pass filter keeps only a selected range of frequencies. It removes very low frequencies and very high frequencies, so the result mainly shows medium-scale structures, textures, and edges.

![Band-stop filter](assets/band_stop.png)

The band-stop filter does the opposite: it removes a selected frequency band and keeps the rest. This can reduce certain repeated patterns or medium-scale details while preserving some smooth regions and some fine details.

### Correlation vs Convolution

```bash
python src/corr_conv.py path/to/your_image.jpg -o assets/corr_conv.png
```

![Correlation vs convolution](assets/corr_conv.png)

This example compares correlation and convolution with an asymmetric kernel. Correlation applies the kernel as it is, while convolution flips the kernel before applying it. With symmetric kernels the results are the same, but with asymmetric kernels the outputs are shifted in different directions.

![Correlation vs convolution difference](assets/corr_conv_diff.png)

The difference image makes the effect easier to see. Bright regions show where the correlation and convolution results are not equal.

### Sampling and Quantization

```bash
python src/sampling.py path/to/your_image.jpg -o assets/sampling.png
```

![Sampling](assets/sampling.png)

This example shows the effect of reducing the number of intensity levels. With fewer bits, the image can represent fewer gray values. The 4-bit, 2-bit, and 1-bit versions show increasing quantization artifacts because smooth intensity changes become large visible steps.

### Mean Filtering

```bash
python src/mean_filter.py path/to/your_image.jpg -o assets/mean_filter.png
```

![Mean filter](assets/mean_filter.png)

Mean filtering replaces each pixel with the average of its surrounding pixels. This smooths the image and reduces small local variations, but it can also blur edges because all pixels in the neighborhood are weighted equally.

### Laplace Filtering

```bash
python src/laplace_filter.py path/to/your_image.jpg -o assets/laplace_filter.png
```

![Laplace filter](assets/laplace_filter.png)

The Laplace filter is a second-derivative edge detector. It responds strongly where the image intensity changes rapidly. Compared with Sobel filtering, it is more sensitive to fine details and noise because second derivatives amplify rapid changes.

### Synthetic Cosine Patterns

```bash
python src/cos_patterns.py -o assets/cos_patterns.png
```

![Cosine patterns](assets/cos_patterns.png)

This example creates synthetic cosine images and shows their Fourier spectra. A cosine pattern appears as two symmetric bright points in the Fourier domain. Vertical stripes create horizontal frequency points, horizontal stripes create vertical frequency points, and diagonal stripes create diagonal frequency points.

## Topics Covered

- Image loading and grayscale conversion
- Sampling and quantization basics
- Mean filtering
- Gaussian filtering
- Correlation vs convolution
- Sobel edge detection
- Laplace filtering
- Fourier spectrum visualization
- Synthetic cosine patterns
- Low-pass filtering in the Fourier domain
- High-pass filtering in the Fourier domain
- Gaussian low-pass filtering
- Band-pass filtering
- Band-stop filtering

## Requirements

The scripts use:

```text
numpy
scipy
matplotlib
```

Install the dependencies with:

```bash
pip install -r requirements.txt
```

Or, using a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run an image-based script by passing the image path as an argument:

```bash
python src/sobel_filter.py path/to/your_image.jpg
```

To save the output figure instead of opening a Matplotlib window, use `-o` or `--output`:

```bash
python src/sobel_filter.py path/to/your_image.jpg -o assets/sobel_filter.png
```

The script `src/cos_patterns.py` creates synthetic cosine-pattern images, so it does not need an external image file:

```bash
python src/cos_patterns.py
```

or:

```bash
python src/cos_patterns.py -o assets/cos_patterns.png
```

Each script opens a Matplotlib window if no output path is provided.

## Fourier-Domain Workflow

The Fourier-domain examples follow this general workflow:

```text
image
-> FFT
-> shift zero frequency to the center
-> create frequency mask
-> apply mask
-> inverse shift
-> inverse FFT
-> filtered image
```

In the shifted Fourier spectrum:

```text
center = low frequencies
far from center = high frequencies
```

This makes it possible to create masks such as low-pass, high-pass, band-pass, and band-stop filters.

## Visualization Notes

Some filters produce positive and negative values. For example:

- high-pass filters
- band-pass filters
- Sobel filters
- Laplace filters

For visualization, these results are sometimes displayed using absolute values.

## Code Quality

This repository uses `pre-commit` and `ruff` for basic code checks and formatting.

Run all checks manually with:

```bash
pre-commit run --all-files
```

## Purpose

This repository is mainly for learning and experimenting with image processing concepts in Python.
