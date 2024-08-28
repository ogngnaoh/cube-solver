# Rubik's Cube Solver Using OpenCV and the Kociemba Library

## Overview

This project implements a Rubik's Cube solver that utilizes computer vision to detect the colors on the cube's faces and then solves the cube using the Kociemba algorithm. The project leverages Python and OpenCV for image processing and contour detection, combined with the Kociemba library to determine the optimal sequence of moves to solve the cube.

## Features

- **Color Detection:** Uses OpenCV to capture and process images of the Rubik's Cube, detecting the colors on each face.
- **Contour Detection:** Identifies the boundaries of each sticker on the cube using edge detection and contour approximation.
- **Face Mapping:** Maps the detected colors to their corresponding faces and converts the color-based representation to the Kociemba-compatible format.
- **Cube Solving:** Generates the optimal sequence of moves to solve the Rubik's Cube using the Kociemba algorithm.

## How It Works

1. **Image Capture and Preprocessing:**
   - The program captures images of the Rubik's Cube, which can be static images or real-time feed from a camera.
   - The images are preprocessed using techniques such as Gaussian blur, edge detection (Canny), and contour detection to identify the stickers on each face.
   - Contours are sorted by using the moments of the contours to calculate the centroid coordinates, which are then sorted to return a top-left to bottom-right order.

2. **Color Classification:**
   - Each detected sticker is classified by its color using HSV color space. The detected colors are then mapped to the cube's orientation, where each face is identified by its center color (e.g., white for the Up face).
   - To ensure accuracy, colors are detected using the largest area of a color detected, to ensure that the most prominent color is chosen for higher accuracy.

3. **Face Ordering and Cube State Construction:**
   - The colors of the stickers are ordered to match the standard Rubik's Cube notation: Up (U), Right (R), Front (F), Down (D), Left (L), and Back (B).
   - The color-based cube state is then converted into a string of face labels (U, R, F, D, L, B) that the Kociemba algorithm can interpret.

4. **Solving the Cube:**
   - The cube state string is passed to the Kociemba library, which returns the optimal sequence of moves to solve the Rubik's Cube.

## Installation

To run this project locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ogngnaoh/cube-solver.git
   cd cube-solver
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. **Install the Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Project:**
   ```bash
   python main.py
   ```

## Usage

1. **Capture Cube Faces:**
   - Ensure the Rubik's Cube is positioned so that the camera or image input can clearly capture each face.
   - Upload the images to a directory and have images labelled according to their orientation

2. **Solve the Cube:**
   - After detecting all the faces, the program will output the sequence of moves required to solve the cube.
   - Follow the provided moves to solve the Rubik's Cube.

## Project Structure

- **`main.py`**: The main script that coordinates the solving processes.
- **`preprocess.py`**: Handles the image processing and color detection of the faces and returns a list of all the classified colors in a data structure to be passed on to the cube state builder
- **`docs`**: Details the explanations and key learnings I came across during the making of this project
- **`check_square.py`**: Ensures that only contours with 4 vertices, roughly same side lengths, and all containing angles close to 90 degrees are added to the contour list for further processing
- **`color_extraction.py`**: Extracts the colors of the contours detected that lie in the HSV ranges specified in colors.py
- **`filter_contours.py`**: Removes further noise from contours such as squares that are too small and fall under an area threshold, or contours that are squares inside of other squares
- **`find_optimal_hsv.py`**: Used during testing stages where I use trackbars to accurately fine-tune and narrow down the most optimal HSV ranges to detect each color accurately

## Contributing

Contributions are welcome! If you have ideas for improvements or want to fix issues, feel free to open a pull request.
