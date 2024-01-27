import numpy as np
import cv2
import matplotlib.pyplot as plt
# Convert the new image to numpy array for processing
new_image_np = np.array(new_image)

# Draw a rectangle around the matched region using the new template
image_with_new_template_bounds = new_image_np.copy()
cv2.rectangle(image_with_new_template_bounds, top_left_new_template, bottom_right_new_template, (0, 255, 0), 2)

# Display the image with the rectangle
plt.imshow(image_with_new_template_bounds)
plt.axis('off')
plt.show()
# Extract the region below the matched text to identify the colored bar
roi_below_new_template = new_image_gray[bottom_right_new_template[1]:bottom_right_new_template[1]+150, 
                                       top_left_new_template[0]-100:bottom_right_new_template[0]+100]

# Threshold the region below the text to identify the colored bar
_, binary_below_new_template = cv2.threshold(roi_below_new_template, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Find contours in the binary image
contours_below_new_template, _ = cv2.findContours(binary_below_new_template, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort contours by width to get the largest contour which should correspond to the colored bar
contours_below_new_template = sorted(contours_below_new_template, key=lambda c: cv2.boundingRect(c)[2], reverse=True)

# Get the bounding rectangle for the largest contour
x, y, w, h = cv2.boundingRect(contours_below_new_template[0])

# Determine the left and right bounds of the colored bar relative to the original image
left_bound = top_left_new_template[0] - 100 + x
right_bound = left_bound + w

# Draw the determined bounds on the image
image_with_bounds = new_image_np.copy()
cv2.line(image_with_bounds, (left_bound, 0), (left_bound, new_image_np.shape[0]), (0, 255, 0), 2)
cv2.line(image_with_bounds, (right_bound, 0), (right_bound, new_image_np.shape[0]), (0, 255, 0), 2)

# Display the image with the determined bounds
plt.imshow(image_with_bounds)
plt.axis('off')
plt.show()
# Extract the region below the colored bar to find the window example
roi_below_bar = new_image_gray[bottom_right_new_template[1]+h:bottom_right_new_template[1]+h+500, left_bound:right_bound]

# Threshold the region to identify potential windows
_, binary_below_bar = cv2.threshold(roi_below_bar, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Find contours in the binary image
contours_windows, _ = cv2.findContours(binary_below_bar, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort contours by area to get the largest contour which should correspond to the window example
contours_windows = sorted(contours_windows, key=cv2.contourArea, reverse=True)

# Get the bounding rectangle for the largest contour
x, y, w, h_window = cv2.boundingRect(contours_windows[0])

# Determine the bottom bound of the window relative to the original image
bottom_bound = bottom_right_new_template[1] + h + y + h_window

# Draw the determined bottom bound on the image
cv2.line(image_with_bounds, (0, bottom_bound), (new_image_np.shape[1], bottom_bound), (0, 255, 0), 2)

# Display the image with the determined bounds
plt.imshow(image_with_bounds)
plt.axis('off')
plt.show()