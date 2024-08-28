import cv2 as cv
import numpy as np


# extracting ROIs to set up cube state
def extract_roi(image, contours):
    rois = []
    # extracts ROIs
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)

        roi = image[y: y + h, x: x + w]

        rois.append(roi)

    return rois


# calculates centroid (center of mass) of a contour
def calculate_centroid(contour):
    M = cv.moments(contour)

    centroid_x = int(M["m10"] / M["m00"])
    centroid_y = int(M["m01"] / M["m00"])

    return centroid_x, centroid_y


# sorting contours to represent the cube state
def sort_contours(contours):
    # calculate centroid for each contour
    centroids = [calculate_centroid(contour) for contour in contours]

    # sorts by y centroid coordinate in list of contours
    contours_centroids = sorted(zip(contours, centroids), key=lambda c: c[1][1])

    sorted_contours = []
    current_row = []
    threshold_y = None
    threshold_h = None

    for contour, centroid in contours_centroids:
        _, y, _, h = cv.boundingRect(contour)
        _, centroid_y = centroid

        # for the first contour only
        if threshold_y is None:
            threshold_y = y
            threshold_h = h
            current_row.append(contour)
        else:
            # checks if the y coordinate of the contours are in the same row, if they are, append to current row
            if abs(centroid_y - threshold_y) <= threshold_h:
                current_row.append(contour)

            # sorts row by x-coordinates
            else:
                current_row.sort(key=lambda contour: calculate_centroid(contour)[0])
                sorted_contours.extend(current_row)
                current_row = [contour]

            threshold_y = centroid_y
            threshold_h = h

    if current_row:
        current_row.sort(key=lambda contour: calculate_centroid(contour)[0])
        sorted_contours.extend(current_row)

    return sorted_contours


# used to classify colors based on where they fall in the HSV ranges
def classify_color(rois, color_ranges):
    classified_colors = []

    for roi in rois:

        hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        max_area = 0
        detected_color = None

        for color, (lower, upper) in color_ranges.items():
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")

            # create mask for current color range
            mask = cv.inRange(hsv_roi, lower, upper)

            # calculate area for this mask
            area = cv.countNonZero(mask)

            if area > max_area:
                max_area = area
                detected_color = color

        classified_colors.append(detected_color)

    return classified_colors


def check_sorting(image, contours):
    for i, contour in enumerate(contours):
        cv.drawContours(image, [contour], -1, (0, 255, 0), 2)

        cx, cy = calculate_centroid(contour)

        cv.putText(image, str(i), (cx, cy), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
