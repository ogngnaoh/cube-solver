import cv2 as cv
import numpy as np
import os
from paths import image_dir


# finding optimal hsv ranges for images
def nothing(x):
    pass


image_paths = []
for file in os.listdir(image_dir):
    file_path = os.path.join(image_dir, file)
    image_paths.append(file_path)

images = [cv.imread(image_path) for image_path in image_paths]

# resizing the image
scale_percent = 0.2
resized_images = []
for image in images:
    width = int(image.shape[1] * scale_percent)
    height = int(image.shape[0] * scale_percent)
    dimensions = (width, height)
    resized_images.append(cv.resize(image, dimensions, interpolation=cv.INTER_AREA))

# initializing sliders to adjust and find optimal hsv range
cv.namedWindow('Trackbars')

cv.createTrackbar('Lower H', 'Trackbars', 0, 179, nothing)
cv.createTrackbar('Lower S', 'Trackbars', 0, 255, nothing)
cv.createTrackbar('Lower V', 'Trackbars', 0, 255, nothing)
cv.createTrackbar('Upper H', 'Trackbars', 179, 179, nothing)
cv.createTrackbar('Upper S', 'Trackbars', 255, 255, nothing)
cv.createTrackbar('Upper V', 'Trackbars', 255, 255, nothing)

while True:

    lower_h = cv.getTrackbarPos('Lower H', 'Trackbars')
    lower_s = cv.getTrackbarPos('Lower S', 'Trackbars')
    lower_v = cv.getTrackbarPos('Lower V', 'Trackbars')
    upper_h = cv.getTrackbarPos('Upper H', 'Trackbars')
    upper_s = cv.getTrackbarPos('Upper S', 'Trackbars')
    upper_v = cv.getTrackbarPos('Upper V', 'Trackbars')

    lower_bound = np.array([lower_h, lower_s, lower_v])
    upper_bound = np.array([upper_h, upper_s, upper_v])

    for i, resized_image in enumerate(resized_images):
        hsv_image = cv.cvtColor(resized_image, cv.COLOR_BGR2HSV)

        mask = cv.inRange(hsv_image, lower_bound, upper_bound)

        result = cv.bitwise_and(resized_image, resized_image, mask=mask)

        cv.imshow(f'Image {i + 1}', resized_image)
        cv.imshow(f'Mask {i + 1}', mask)
        cv.imshow(f'Result {i + 1}', result)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
