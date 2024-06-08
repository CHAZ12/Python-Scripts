import pygetwindow
import time
import pyautogui
import PIL
import pyautogui

import PIL
from PIL import Image
import cv2
from pytesseract import pytesseract, Output
import numpy as np
import matplotlib.pyplot as plt
import random

# py -m pip install numpy exmaple for package
# Get the Runelite Window and take a screenShot
def GetWindow():
    Timer = 0
    Timer+=1
    if(Timer == 40):
        print("script Reached it max duration")
        quit()
        
    # Get window size
    print("Get Window")
    x2,y2 = pyautogui.size(); x2,y2=int(str(x2)),int(str(y2))
    my = pygetwindow.getWindowsWithTitle("RuneLite")[0]
    # Quarter of screen screensize
    x3 = x2 // 2; y3 = y2 // 2
    my.resizeTo(x3,y3)
    # Top-left
    my.moveTo(0, 0)
    time.sleep(3)
    my.activate()
    time.sleep(1)
    # save screenshot
    p = pyautogui.screenshot()
    p.save(r'C:\\Users\\zpmas\\OneDrive\\Pictures\\RuneLite.png')
    # edit screenshot to size of desired window
    im = PIL.Image.open('C:\\Users\\zpmas\\OneDrive\\Pictures\\RuneLite.png')
    im_crop = im.crop((0, 0, x3, y3))
    im_crop.save('C:\\Users\\zpmas\\OneDrive\\Pictures\\RuneLite.png', quality=100)
    print('ScreenShot saved')
    ReadImage()

def ReadImage():
    print("Read Image")
    # Opening/Reading image
    pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    img = cv2.imread('C:\\Users\\zpmas\\OneDrive\\Pictures\\RuneLite.png')
    DetectFishing()
    
from PIL import Image
    
def DetectFishing():
    print("Is User Fishing?")
    img = cv2.imread('C:\\Users\\zpmas\\OneDrive\\Pictures\\RuneLite.png')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 255, 255])
    upper = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    #cv2.imshow('', mask)
    #cv2.waitKey(0)
    results = pytesseract.image_to_data(mask, output_type=Output.DICT, config="--psm 6")
    for i in range(len(results["text"])):
        # Extract the OCR text itself along with the confidence of the
        text = results["text"][i]
        #print(text)
        if(text == "NOT" or text == "MOT"):
            print("User is not fishing")
            DetectInv()
            #Detectfish()
            break
        elif(text == "Fishing"):
            print("User is already fishing, waiting some time to pass")
            time.sleep(20 + random.uniform(10.34,23.4))
            GetWindow()
            break
    #DetectInv()

def Detectfish():
    print("Find Fishing Spot")
    # Find Trout color
    img = cv2.imread('C:\\Users\\zpmas\\OneDrive\\Pictures\\RuneLite.png')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([86, 207, 0]), np.array([95, 255, 247]))
    green = np.zeros_like(img, np.uint8)
    green[mask>0] = img[mask>0]
    cv2.imwrite('C:\\Users\\zpmas\\OneDrive\\Pictures\\Fishmask.png', green)
    print("saved image")
    imgmask = Image.open('C:\\Users\\zpmas\\OneDrive\\Pictures\\Fishmask.png')
    imgmask = imgmask.convert("RGB")
    #plt.imshow(imgmask)
    #plt.show()
    w, h = imgmask.width-1, imgmask.height-1
    # Convert color array into coordinates
    found = 0
    for x in reversed(range(w)):
        for y in reversed(range(h)):
            if imgmask.getpixel((x,y))[1] >= 170 and found ==0 and x <600: #(23, 161, 170)
                print("Found spot at "  + str(x) + ","+ str(y)) 
                found = 1
                MoveMouse(x-20 + random.randint(-2,2),y-12)
                break
        if found == 1:
            break
    if found == 0:
        time.sleep(30 + random.randint(-10,10))
        GetWindow()      
    #cv2.imshow('', green), 
    #cv2.waitKey(0)

def MoveMouse(xpos,ypos):
    print("Moved Mouse", xpos, ypos)
    pyautogui.moveTo(xpos, ypos, duration = 1)
    time.sleep(1)
    pyautogui.click(xpos, ypos)
    print("On cool down...")
    time.sleep(30 + random.randint(-10,10))
    GetWindow()
      
def DetectInv():
    # Detect fish in inventory
    print("Checking Full Inventory")          
    img = cv2.imread('C:\\Users\\zpmas\\OneDrive\\Pictures\\Fishmask.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(gray, np.array([14, 75, 8]), np.array([18, 101, 67]))
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)
    #cv2.imshow("Shapes", mask)
    #cv2.waitKey(0)
    edges = cv2.Canny(blurred, 10, 255)
    contours,hierarchy = cv2.findContours(edges, 1, 1)
    cv2.imwrite('C:\\Users\\zpmas\\OneDrive\\Pictures\\Inventorymask.png', mask)
    for cnt in contours:
        x1,y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.002*cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(cnt)
            ratio = float(w)/h
            if ratio >= 0.9 and ratio <= 1.2:
                pass
            else:
                if w >10:
                    mask = cv2.drawContours(img, [cnt], -1, (0,255,0), 3)
                    #print(str(w) + ":w, " + str(h) + ":h \n" + str(x) + ":x, " + str(y) + ":y")
            
                    # divide by inventory slots
                    width = w/5
                    height = h/7
                    top = height + y
                    bottom = width + x
                    i=1;j=7
                    LTR = int((width*i ) + x-8) # Left to right
                    TTB = int((height*j) + y-20) # Top to bottom
                    im = Image.open(r'C:\\Users\\zpmas\\OneDrive\\Pictures\\Inventorymask.png')
                    bob = im.convert("L")
                    bob.show()
                    color = bob.getpixel((LTR,TTB))
                    print(color)
                    if(color == 255):
                        print("Not Full")  
                        Detectfish()
                    else:
                        print("Inventory Full")
                        RN = random.randint(1,2)
                        if(RN == 1):
                            Across(width, height, x, y, img)
                        else:
                            ZigZag(width, height, x, y, img)
def Across(width, height, x, y, img):
    #Across and Down
    j=0; i=1
    for a in range(7):
        i=1; j+=1 
        for b in range(4):
            LTR = int((width*i ) + x-4) # Left to right
            TTB = int((height*j) + y-14) # Top to bottom
            pyautogui.moveTo(LTR,TTB, duration=.15+random.uniform(-.2,.1))
            cv2.circle(img,(LTR,TTB), 10, (255,0,0),1)
            i+=1
    time.sleep(30 + random.randint(-10,10))
    GetWindow()
    
def ZigZag(width, height, x, y, img):
    # ZigZag
                    j=7; i=1;r=8
                    for a in range(4):
                        if(a == 0):
                            j = 1; i = 1
                        elif(a == 1):
                            j = 3; i= 1
                        elif(a == 2):
                            j = 5; i = 1
                        elif(a == 3):
                            j= 7; i= 1; r= 4    
                        for b in range(r):
                            LTR = int((width*i ) + x - 4 + random.randint(-3,4)) # Left to right
                            TTB = int((height*j) + y - 20 + random.randint(-3,5)) # Top to bottom
                            pyautogui.moveTo(LTR,TTB, duration=.102)
                            cv2.circle(img,(LTR,TTB), 10, (255,0,0),1)
                            if(a==3):
                                i+=1
                            elif(j+1 == 2 or j+1 == 4 or j+1 == 6):
                                j+=1
                            else:
                                i+=1; j-=1
                        print("On cool down...")
                        time.sleep(30 + random.randint(-10,10))
                        print("Resettting...")
                        GetWindow() 
#GetWindow()
#DetectFishing()
#ReadImage()
DetectInv()
    