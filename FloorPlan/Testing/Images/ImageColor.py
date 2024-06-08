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
# Save image in set directory
# Read RGB image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# Read Images
image = cv2.imread('House1.PNG')
image = cv2.resize(image, (1400, 1400))
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
lower_blue = np.array([0, 0, 0])
upper_blue = np.array([22, 12, 11])

mask = cv2.inRange(image, lower_blue, upper_blue)
edge = cv2.Canny(mask, 100, 400)

lines = cv2.HoughLinesP(edge, rho=1, theta=1 * np.pi / 180, threshold=50, minLineLength=1, maxLineGap=90)
for i in lines:
    x1,x2,y1,y2=i[0]
    cv2.line(image,(x1,x2),(y1,y2), (0,255,0),6)

#plt.imshow(mask)
#plt.imshow(image)
#plt.show()
from PIL import Image
Image.fromarray(image).save('mask1.PNG')
BotList = open("NewBotList.txt", "w+")
print("Finished")



