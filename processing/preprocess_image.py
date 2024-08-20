import os
from check_square import is_square
import cv2 as cv
import numpy as np
from filter_contours import filter_contours, remove_child_squares
from color_extraction import sort_contours, extract_roi, classify_color, check_sorting
from colors import color_ranges


def preprocess_image(image_path):
    # loads the image
    image = cv.imread(image_path)
    image_size = image.shape[:2]

    # grayscale, reducing noise with gaussian filter, detecting edges with canny edge algorithm
    grayscale_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(grayscale_img, (5, 5), 0)
    edges = cv.Canny(blurred, 20, 30)

    # dilate to smooth out the edges and connect the fragmented ones into a closed loop
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv.dilate(edges, kernel, iterations=3)

    # find contours
    contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # make copy so that contours can be drawn without affecting the original image
    image_with_contours = image.copy()

    # processing the contours to separate the cube stickers from the rest of the noise
    approximated_contours = []

    for contour in contours:
        epsilon = 0.12 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        if is_square(approx):
            approximated_contours.append(approx)

    # remove the small contours that are background noise
    filtered_contours = filter_contours(approximated_contours)

    # remove child squares from contours
    final_contours = remove_child_squares(filtered_contours, image_size)

    # sort the colours out according to a top left to bottom right orientation
    sorted_contours = sort_contours(final_contours)

    # draw contours on copied image
    rois = extract_roi(image, sorted_contours)
    classified_colours = classify_color(rois, color_ranges)

    return classified_colours
    # return image_with_contours


image_dir = r'C:\Users\ngovi\OneDrive\Desktop\cv_project\cube_faces'
processed_dir = r'C:\Users\ngovi\OneDrive\Desktop\cv_project\processed_cube_faces'

for filename in os.listdir(image_dir):
    image_path = os.path.join(image_dir, filename)
    print(preprocess_image(image_path))
    # processed_image = preprocess_image(image_path)
    # base_name = os.path.splitext(filename)[0]
    # new_filename = f'{base_name}_processed.jpg'
    # cv.imwrite(os.path.join(processed_dir, new_filename), processed_image)
