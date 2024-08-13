The values chosen for the Gaussian filter parameters and Canny edge detection parameters are critical for achieving the desired balance between noise reduction and edge detection sensitivity. Here's the reasoning behind the choices:

### 1. **Gaussian Filter Parameters**

The Gaussian filter is used to blur the image, which helps reduce noise and minor details, making edge detection more robust. The key parameters are the kernel size and the standard deviation (sigma).

- **Kernel Size (5x5):**
  - **Reasoning:** The kernel size determines the area over which the filter is applied. A 5x5 kernel size is a common choice that provides a good balance between smoothing and retaining important features. It's large enough to reduce noise but not so large that it overly blurs the image.
  - **Effect:** If the kernel size is too small (e.g., 3x3), it may not adequately reduce noise. If it's too large (e.g., 7x7 or more), it may blur important edges, making them harder to detect later.
  - **Formula:** The kernel size is usually chosen as an odd number (e.g., 3x3, 5x5) to ensure that there is a center pixel for the filter to focus on.

- **Standard Deviation (sigma = 0):**
  - **Reasoning:** The standard deviation determines the spread of the Gaussian function. In OpenCV, setting sigma to 0 lets the function automatically calculate it based on the kernel size. This automatic calculation usually works well for typical applications.
  - **Effect:** A smaller sigma would result in less blurring, while a larger sigma would result in more blurring. By setting it to 0, the blurring effect is optimized for the chosen kernel size.
