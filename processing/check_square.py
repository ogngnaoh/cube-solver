import numpy as np


# checks if the contour is square
def is_square(approx):
    if len(approx) != 4:
        return False

    def side_length(p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    side_lengths = [
        side_length(approx[0][0], approx[1][0]),
        side_length(approx[1][0], approx[2][0]),
        side_length(approx[2][0], approx[3][0]),
        side_length(approx[3][0], approx[0][0])
    ]

    avg_length = np.mean(side_lengths)
    for length in side_lengths:
        if abs(length - avg_length) > 0.1 * avg_length:
            return False

    def angle(p1, p2, p3):
        v1 = np.array(p1) - np.array(p2)
        v2 = np.array(p3) - np.array(p2)
        cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle_rad = np.arccos(cosine_angle)
        angle_deg = np.degrees(angle_rad)
        return angle_deg

    angles = [
        angle(approx[0][0], approx[1][0], approx[2][0]),
        angle(approx[1][0], approx[2][0], approx[3][0]),
        angle(approx[2][0], approx[3][0], approx[0][0]),
        angle(approx[3][0], approx[0][0], approx[1][0])
    ]

    for angle in angles:
        if abs(angle - 90) > 10:
            return False

    return True
