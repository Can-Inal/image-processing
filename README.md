# Image Processing Experiments

This repository contains small Python scripts for learning and experimenting with basic image processing concepts.

The examples cover spatial-domain filtering, Fourier-domain filtering, edge detection, sampling, and synthetic frequency patterns.

The repository does not include an input image. To run the image-based scripts, use your own image file and pass its path as a command-line argument.

## Topics Covered

* Image loading and grayscale conversion
* Sampling and quantization basics
* Mean filtering
* Gaussian filtering
* Correlation vs convolution
* Sobel edge detection
* Laplace filtering
* Fourier spectrum visualization
* Synthetic cosine patterns
* Low-pass filtering in the Fourier domain
* High-pass filtering in the Fourier domain
* Gaussian low-pass filtering
* Band-pass filtering
* Band-stop filtering

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

Run an image-based script by passing the image path as an argument.

Example:

```bash
python src/sobel_filter.py path/to/your_image.jpg
```

or:

```bash
python src/fourier_spectrum.py path/to/your_image.jpg
```

The script `src/cos_patterns.py` creates synthetic cosine-pattern images, so it does not need an external image file:

```bash
python src/cos_patterns.py
```

Each script opens a Matplotlib window showing the result of the corresponding image processing operation.

## Script Overview

### `src/sampling.py`

Demonstrates basic sampling-related image operations.

### `src/mean_filter.py`

Applies a mean filter to smooth an image.

### `src/gaussian_filter.py`

Applies Gaussian smoothing in the spatial domain.

### `src/corr_conv.py`

Compares correlation and convolution using an asymmetric kernel.

### `src/sobel_filter.py`

Applies Sobel filters in x- and y-direction and computes the gradient magnitude.

### `src/laplace_filter.py`

Applies a Laplace filter for second-derivative edge detection.

### `src/fourier_spectrum.py`

Computes and visualizes the Fourier magnitude spectrum of an image.

### `src/cos_patterns.py`

Creates synthetic cosine patterns and visualizes their Fourier spectra.

### `src/low_pass_filter.py`

Applies an ideal low-pass filter in the Fourier domain.

### `src/high_pass_filter.py`

Applies an ideal high-pass filter in the Fourier domain.

### `src/gaussian_low_pass_filter.py`

Applies a Gaussian low-pass filter in the Fourier domain.

### `src/band_pass_filter.py`

Keeps only a selected frequency band in the Fourier domain.

### `src/band_stop_filter.py`

Removes a selected frequency band in the Fourier domain.

## Fourier-Domain Workflow

The Fourier-domain examples follow this general workflow:

```text
image
→ FFT
→ shift zero frequency to the center
→ create frequency mask
→ apply mask
→ inverse shift
→ inverse FFT
→ filtered image
```

In the shifted Fourier spectrum:

```text
center = low frequencies
far from center = high frequencies
```

This makes it possible to create masks such as low-pass, high-pass, band-pass, and band-stop filters.

## Visualization Notes

Some filters produce positive and negative values. For example:

* high-pass filters
* band-pass filters
* Sobel filters
* Laplace filters

For visualization, these results are sometimes displayed using absolute values.

## Purpose

This repository is mainly for learning and experimenting with image processing concepts in Python.
