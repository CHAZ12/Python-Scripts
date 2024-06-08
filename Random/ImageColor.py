# !/usr/bin/env python3
import subprocess
import sys
import numpy

print('Getting or installing necessary modules')
try:
    import pillow

    print('module pillow is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'pillow'])

try:
    import opencv

    print('module cv2 is installed')
except ModuleNotFoundError:
    print('module cv2 is not installed')
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'opencv-python'])

try:
    import cv2

    print('module cv2 is installed')
except ModuleNotFoundError:
    print('module cv2 is not installed')
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'opencv-python'])
from PIL import Image

# def get_image(image_path):
#     """Get a numpy array of an image so that one can access values[x][y]."""
#     image = Image.open(image_path, "r")
#     width, height = image.size
#     pixel_values = list(image.getdata())
#     if image.mode == "RGB":
#         channels = 3
#     elif image.mode == "L":
#         channels = 1
#     else:
#         print("Unknown mode: %s" % image.mode)
#         return None
#     pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
#     print(pixel_values)
#     return pixel_values
#
#
# image = get_image("House3.PNG")


# Save image in set directory
# Read RGB image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# Read Images
import cv2 as cv

image = cv2.imread('House1.PNG')
image = cv2.resize(image, (1400, 1400))
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
edge = cv2.Canny(image, 350, 450)
lines = cv2.HoughLinesP(edge, rho= 1, theta=1*np.pi/180, threshold=300, minLineLength=100, maxLineGap=10)

#threshold: gap bewteen lines
# minLine:
# maxLine:
for i in lines:
    x1,x2,y1,y2=i[0]
    cv2.line(image,(x1,x2),(y1,y2), (0,255,0),3)

print("The type of this input is {}".format(type(image)))
print("Shape: {}".format(image.shape))
cv2.waitKey(0)
cv2.destroyAllWindows()
plt.imshow(image)
plt.show()
