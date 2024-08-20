import cv2 as cv
import numpy as np


def filter_contours(contours_list, min_area_ratio=0.10):
    # calculate the area of all approximated contours
    approx_contour_area = [cv.contourArea(contour) for contour in contours_list]

    # determine the area of the largest approximated contour
    max_area = max(approx_contour_area)

    # define area thresholds
    min_area_threshold = min_area_ratio * max_area

    # filter approximated contours based on area
    filtered_contours = []

    for contour in contours_list:

        if cv.contourArea(contour) > min_area_threshold:
            filtered_contours.append(contour)

    return filtered_contours


def recalculate_hierarchy(filtered_contours, image_size):
    binary_mask = np.zeros(image_size, dtype=np.uint8)

    cv.drawContours(binary_mask, filtered_contours, -1, 255, thickness=cv.FILLED)

    contours, hierarchy = cv.findContours(binary_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    return contours, hierarchy


def remove_child_squares(filtered_contours, image_size):
    contours, hierarchy = recalculate_hierarchy(filtered_contours, image_size)

    final_contours = []
    for i, contour in enumerate(contours):

        if hierarchy[0][i][3] == -1:
            final_contours.append(contour)

    return final_contours
