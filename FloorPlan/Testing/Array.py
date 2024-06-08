import numpy as np
import cv2
import matplotlib.pyplot as plt

# img = cv2.imread('mask.PNG')
# img = cv2.resize(img, (1400, 1400))
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# #(image, number of corners, 0-1(perfect corner), minimum distance between 2 corners)
# corners = cv2.goodFeaturesToTrack(gray, 500, .4, 20)
# corners - np.int0(corners)
#
# for corner in corners:
#     x, y = corner.ravel()    # ex [[[0, 1, 2]]] -> [0, 1 ,2]
#     cv2.circle(img, (int(x), int(y)), 5, (255, 0, 0), -1)
#     print(x)
#
# plt.imshow(img)
# plt.show()
# #cv2.imshow('Frame', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

from PIL import Image

from PIL import ImageColor

#def find_rgb(imagename, r_query):
img = Image.open('House1.PNG')
img = img.convert("RGB")
#img = img.resize((600,600))
arrayx = open('line_xcoords.txt', 'a+')
arrayx.truncate(0)
w, h = img.width-1, img.height-1
img1 = ImageColor.getrgb("yellow")
d = img.getdata()
new_image = []
for item in d:
    #print(item[0], item[1], item[2])
    if item[0] in list(range(238, 256)) or item[1] not in list(range(0, 30)) or item[2] not in list(range(30,50)): # only leave red
        new_image.append((255, 255, 255))
    else:
        new_image.append(item)

found = 1
img.putdata(new_image)
for x in reversed(range(w)):
    for y in reversed(range(h)):
        if img.getpixel((x,y)) == (237, 28, 36) and found == 1:
            p = img.getpixel((x,y))
            found = 0
            #print(img.getpixel((x, y)))
        if img.getpixel((x, y+1)) != (237, 28, 36) and found == 0:
            #if img.getpixel((x,y+1)) != (237,28,36) and img.getpixel((x,y-4)) != (237,28,36): Find between lines
            if img.getpixel((x,y+2)) != (237,28,36) and img.getpixel((x,y-4)) != (237,28,36):
                print('true')
                img.putpixel((x, y-1), (0, 255, 0))
           # img.putpixel((x, y), (0, 255, 0))
            print(y)
            found = 1
        if img.getpixel((x, y +1)) == (255, 255, 255) and found == 0:
            img.putpixel((x, y-1), (0, 0, 255))

# for x in reversed(range(w)):
#     for y in range(h):
#         if img.getpixel((x,y)) == (237, 28, 36) and found == 1:
#             p = img.getpixel((x,y))
#             found = 0
#             #print(img.getpixel((x, y)))
#         if img.getpixel((x, y)) != (237, 28, 36) and found == 0:
#             img.putpixel((x, y), (0, 255, 0))
#             print(y)
#             found = 1

plt.imshow(img)
plt.show()