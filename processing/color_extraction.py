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

    # converts the color spaces of the ROIs to make it easier to detect the colors and build cube state
    for contour in rois:
        cv.cvtColor(contour, cv.COLOR_BGR2HSV)

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
            if abs(centroid_y - threshold_y) <= threshold_h // 2:
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


def classify_color(rois, color_ranges):
    classified_colors = []

    for roi in rois:
        # gives average hsv values over all the pixels in the bounding box/ROI
        mean_hsv = cv.mean(roi)[:3]

        detected_color = None

        for color, (lower, upper) in color_ranges.items():
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")

            mask = cv.inRange(np.array(mean_hsv, dtype='uint8'), lower, upper)

            if np.any(mask):
                detected_color = color
                break

        classified_colors.append(detected_color)

    return classified_colors


def check_sorting(image, contours):
    for i, contour in enumerate(contours):
        cv.drawContours(image, [contour], -1, (0, 255, 0), 2)

        cx, cy = calculate_centroid(contour)

        cv.putText(image, str(i), (cx, cy), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)

