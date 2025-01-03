import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os
import subprocess
import sys
from termcolor import colored

print('Getting or installing necessary modules')
#   Inorder for the script to run properly you need all modules below, so make sure they are installed
try:
    import termcolor

    print('module termcolor is installed')
except ModuleNotFoundError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'termcolor'])
       
def StartGettingColumns(new_image):
    print("Start Getting Columns")
    img = Image.open(imgDir)
    img = img.convert("RGB")
    current_line = (0, 0)
    first = False
    found_starting_point = 0
    found_line = False
    w, h = img.width-1, img.height-1
    img.putdata(new_image)

    global count
    global vdivide
    
    global currentArray
    currentArray = []
    global finishedColumn
    finishedColumn = False
    
    # Starts at bottom right and goes down to up then moves left
    for x in reversed(range(w)):
        if current_line != (0, 0) and (x > current_line[0] - 2) and found_line:
            found_line = False
        else:
            for y in reversed(range(h)):
                if img.getpixel((x, y)) == (237, 28, 36) and img.getpixel((x - 1, y)) == (237, 28, 36) and img.getpixel((x + 1, y)) == (237, 28, 36) and img.getpixel((x + 1, y - 3)) == (237, 28, 36) and img.getpixel((x - 1, y - 3)) == (237, 28, 36) and found_starting_point == 0:
                    if not first:
                        img.putpixel((x, y - 1), (0, 0, 255))  # Blue
                        first = True
                        found_line = True
                        currentArray.append((x/vdivide,(y-1)/vdivide,0))
                        count +=1
                        #print(currentArray)
                    elif img.getpixel((x - 1, y)) != (0, 0, 255) and img.getpixel((x + 1, y)) != (0, 0, 255):
                        img.putpixel((x, y - 1), (0, 0, 255))  # Blue
                        currentArray.append((x/vdivide,(y-1)/vdivide,0))
                        count += 1
                        #print(currentArray)
                    found_starting_point = 1
                if img.getpixel((x, y)) == (237, 28, 36) and img.getpixel((x - 1, y)) == (237, 28, 36) and img.getpixel((x + 1, y)) == (237, 28, 36) and img.getpixel((x, y - 1)) != (237, 28, 36) and img.getpixel((x, y - 1)) != (0, 0, 255) and img.getpixel((x - 2, y - 1)) != (0, 0, 255) and found_starting_point == 1:
                    img.putpixel((x, y + 1), (0, 255, 0))  # Green
                    found_starting_point = 0
                    currentArray.append((x/vdivide,(y+1)/vdivide,0))
                    count +=1
                    #print(currentArray)
                if y == 3:
                    if found_line:
                        first = False
                        CheckArrayIndex()
                        currentArray.clear()
                        
    finishedColumn = True
    img.convert("RGB").save('C:/Users/zpmas/Building/HouseC.png', "PNG")      
    StartGettingRows(img, new_image)
    
def StartGettingRows(img, new_image):
    print("Start Getting Rows")
    #mg = Image.open('C:/Users/zpmas/Building/House1.PNG')
    currentLine = (0, 0)
    first = False
    foundStartingPoint = 0
    foundLine = False
    w, h = img.width-1, img.height-1
    img.putdata(new_image)
    
    global count
    global vdivide
    
    # Starts at bottom right and goes right to left then moves up
    for y in reversed(range(h)):
        if currentLine != (0, 0) and (y > currentLine[1] - 2) and foundLine:
            foundLine = False
        else:
            for x in reversed(range(w)):
                if img.getpixel((x, y)) == (237, 28, 36) and img.getpixel((x, y-1)) == (237, 28, 36) and img.getpixel((x, y+1)) == (237, 28, 36) and img.getpixel((x-3, y +1)) == (237, 28, 36) and img.getpixel((x - 3, y - 1)) == (237, 28, 36) and foundStartingPoint == 0:  # if the pixel is red mark it as found
                    if first == False:
                        img.putpixel((x-1, y), (0, 0, 255))  # blue
                        first = True
                        foundLine = True
                        currentArray.append(((x-1)/vdivide,y/vdivide,0))
                        count +=1
                    elif img.getpixel((x-1, y)) != (0, 0, 255) and img.getpixel((x+1, y)) != (0, 0, 255):
                        img.putpixel((x-1, y), (0, 0, 255))  # blue
                        currentArray.append(((x-1)/vdivide,y/vdivide,0))
                        count +=1
                    foundStartingPoint = 1
                if img.getpixel((x, y)) == (237, 28, 36) and img.getpixel((x, y-1)) == (237, 28, 36) and img.getpixel((x, y+1)) == (237, 28, 36) and img.getpixel((x-1, y)) != (237, 28, 36) and img.getpixel((x-1, y)) != (0, 0, 255) and img.getpixel((x - 1, y - 2)) != (0, 0, 255) and foundStartingPoint == 1:
                    img.putpixel((x+1, y), (0, 255, 0))  # green
                    foundStartingPoint = 0
                    currentArray.append(((x+1)/vdivide,y/vdivide,0))
                    count +=1
                if x == 3:
                    if foundLine:
                        first = False
                        currentLine = (x, y)
                        CheckArrayIndex()
                        currentArray.clear()
    img.save('C:/Users/zpmas/Building/HouseR.png', "PNG")                    
    #plt.imshow(img)
    #plt.show()
    set_red_to_transparent()                            

def CombineImages():
    print("Combine Images")
    overlay_image_path = Image.open('C:/Users/zpmas/Building/HouseR.png')
    Main_image_path = Image.open('C:/Users/zpmas/Building/HouseC.png')
    combined = Image.alpha_composite(overlay_image_path.convert('RGBA'),Main_image_path.convert('RGBA'))
    combined.convert("RGBA").save('C:/Users/zpmas/Building/HouseFinal.png', "PNG")
    os.remove('C:/Users/zpmas/Building/HouseR.png') # Row output image
    os.remove('C:/Users/zpmas/Building/HouseC.png') # Column ouput image
    print("FINISHED")
    
def set_red_to_transparent():
    print("Set red to Transparent")

    #Set Row values Transparency
    print("Setting Row Image Transparent")      
    img = Image.open('C:/Users/zpmas/Building/HouseR.png') 
    rgba = img.convert("RGBA") 
    datas = rgba.getdata() 
    
    newData = [] 
    for item in datas: 
        # Check if the pixel is close to red
        if item[0] in list(range(238, 256)) or item[1] not in list(range(0, 30)) or item[2] not in list(range(30,50)): # only leave red
            # Store a transparent value when we find a red-like color
            newData.append(item)  # Other colors remain unchanged 
        else: 
            newData.append((255, 255, 255, 0))
            
      
    rgba.putdata(newData) 
    rgba.save("C:/Users/zpmas/Building/HouseR.png", "PNG")
    
    #Set Column values Transparency
    print("Setting Column Image Transparent")    
    img2 = Image.open('C:/Users/zpmas/Building/HouseC.png') 
    rgba = img2.convert("RGBA") 
    datas = rgba.getdata() 
    newData = [] 
    for item in datas: 
        # Check if the pixel is close to red
        if item[0] in list(range(238, 256)) or item[1] not in list(range(0, 30)) or item[2] not in list(range(30,50)): # remove only red
            # Store a transparent value when we find a red-like color
            newData.append(item)  # Other colors remain unchanged 
        else: 
            newData.append((255, 255, 255, 0))
    
    rgba.putdata(newData) 
    rgba.save("C:/Users/zpmas/Building/HouseC.png", "PNG")  
    CombineImages()     
    
    
    
def StartImageProcess():
    if(ResetPointFiles()):
        img = Image.open(imgDir)
        img = img.convert("RGBA")
        d = img.getdata()
        new_image = []
        for item in d:
            if item[0] in list(range(238, 256)) or item[1] not in list(range(0, 30)) or item[2] not in list(range(30,50)): # only leave red
                new_image.append((255, 255, 255, 0))
            else:
                new_image.append(item)
        #plt.imshow(img)
        #plt.show()
        
        StartGettingColumns(new_image)
    
def CheckArrayIndex():
    if len(currentArray) != 0:
        if(not finishedColumn):
            colunmnFile =  open("C:/Users/zpmas/Building/ColumnValues.txt", "a+")
            colunmnFile.write(str(currentArray).strip("[]") + "\n")
        else:
            rowFile =  open("C:/Users/zpmas/Building/RowValues.txt", "a+")
            rowFile.write(str(currentArray).strip("[]")+ "\n")
            
            
def ResetPointFiles():
    print("Deleting Old Point Files")
    if os.path.exists("C:/Users/zpmas/Building/ColumnValues.txt"):
        with open("C:/Users/zpmas/Building/ColumnValues.txt") as f:
            f.close()
        os.remove("C:/Users/zpmas/Building/ColumnValues.txt")
    if os.path.exists("C:/Users/zpmas/Building/RowValues.txt"):
        with open("C:/Users/zpmas/Building/RowValues.txt") as f:
            f.close()
        os.remove("C:/Users/zpmas/Building/RowValues.txt")
    if os.path.exists(imgDir):
        return True
    else:
        print(colored(f"File Does not exist:{imgDir}",'red'))
        return False
    
                
count = 0
vdivide = 10
imgDir = 'C:/Users/zpmas/Building/House20a.png'
StartImageProcess()    

# \((.*?)\) capture everthing inside "()"