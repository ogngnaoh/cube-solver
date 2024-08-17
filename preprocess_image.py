import os
from check_square import is_square
import cv2 as cv
import numpy as np


def preprocess_image(image_path):
    # loads the image
    image = cv.imread(image_path)

    # grayscale, reducing noise with gaussian filter, detecting edges with canny edge algorithm
    grayscale_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(grayscale_img, (3, 3), 0)
    edges = cv.Canny(blurred, 20, 40)

    # dilate to smooth out the edges and connect the fragmented ones into a closed loop
    kernel = np.ones((4, 4), np.uint8)
    dilated = cv.dilate(edges, kernel, iterations=4)

    # find contours
    contours, hierarchy = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # make copy so that contours can be drawn without affecting the original image
    image_with_contours = image.copy()

    # processing the contours to separate the cube stickers from the rest of the noise
    for contour in contours:
        epsilon = 0.08 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        if is_square(approx):
            cv.drawContours(image_with_contours, [approx], -1, (0, 255, 0), 4)

    return image_with_contours


image_dir = r'C:\Users\ngovi\OneDrive\Desktop\cv_project\cube_faces'
processed_dir = r'C:\Users\ngovi\OneDrive\Desktop\cv_project\processed_cube_faces'
processed_images = []

for filename in os.listdir(image_dir):
    image_path = os.path.join(image_dir, filename)
    processed_image = preprocess_image(image_path)
    processed_images.append(processed_image)
    base_name = os.path.splitext(filename)[0]
    new_filename = f'{base_name}_processed.jpg'
    cv.imwrite(os.path.join(processed_dir, new_filename), processed_image)
