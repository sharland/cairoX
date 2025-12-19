import numpy as np
import math
from random import *
import os, sys
from PIL import Image, ImageOps
import time

try:
    import cairo
except:
    import cairocffi as cairo

#not working
'''
def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

'''

'''
Used to calculate the angle between two points where each point is a combination of an x and y coordinate
'''
def angleBetween(p1, p2):
    myradians = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
    mydegrees = math.degrees(myradians)
    return mydegrees

def endPoint(p1,ang,d):         #working
    a = math.radians(ang)
    endX,endY = p1[0]+(d*math.sin(a)),p1[1]+(d*math.cos(a))
    return endX,endY

def fibCreate(w,h):             #working
    gen = True
    fibseq = [0,1]
    while gen == True:
        new = sum(fibseq[-2:])
        if new < w*h:
            fibseq.append(new)
        else:
            gen = False
    return fibseq

def background(r,g,b,w,h,surface):
    context = cairo.Context(surface) 
    context.set_source_rgb(r/255, g/255, b/255)
    context.rectangle(0, 0, h, w)
    return context.fill()

def gradientDirection():    #call this once

    #figure out direction if hit colour limit
    redChoice = randint(0,1)
    if redChoice == 0:
        redDirection = False
    else:
        redDirection = True

    greenChoice = randint(0,1)
    if greenChoice == 0:
        greenDirection = False
    else:
        greenDirection = True

    blueChoice = randint(0,1)
    if blueChoice == 0:
        blueDirection = False
    else:
        blueDirection = True

    widthChoice = randint(0,1)
    if widthChoice == 0:
        widthDirection = False
    else:
        widthDirection = True
    
    opacityChoice = randint(0,1)
    if opacityChoice == 0:
        opacityDirection = False
    else:
        opacityDirection = True

    return redDirection,greenDirection,blueDirection,widthDirection,opacityDirection

def gradientColour(redDirection,greenDirection,blueDirection,widthDirection,opacityDirection,colourChange,widthChange,opacityChange,penWidth,randomRed,randomGreen,randomBlue,randomWidth,randomOpacity):       #will need to call this in the loop
    if redDirection == True:
        randomRed += colourChange
        if randomRed >= 1.0:
            redDirection = False
            
    if redDirection == False:
        randomRed -= colourChange
        if randomRed <= 0:
            redDirection = True

    if greenDirection == True:
        randomGreen += colourChange
        if randomGreen >= 1:
            greenDirection = False
    if greenDirection == False:
        randomGreen -= colourChange
        if randomGreen <= 0:
            greenDirection = True

    if blueDirection == True:
        randomBlue += colourChange
        if randomBlue >= 1:
            blueDirection = False
    if blueDirection == False:
        randomBlue -= colourChange
        if randomBlue <= 0:
            blueDirection = True

    if widthDirection == True:
        randomWidth += widthChange
        if randomWidth >= penWidth:
            widthDirection = False
    if widthDirection == False:
        randomWidth -= widthChange
        if randomWidth <= 0:
            widthDirection = True

    if opacityDirection == True:
        randomOpacity += opacityChange
        if randomOpacity >= 1:
            opacityDirection = False
    if opacityDirection == False:
        randomOpacity -= opacityChange
        if randomOpacity <= 0:
            opacityDirection = True

    return randomRed,randomGreen,randomBlue,randomOpacity,randomWidth,redDirection,greenDirection,blueDirection,widthDirection,opacityDirection

def detail(gapSize):
    quality = [int(val) for val in range(0,256, gapSize)]
    #print(quality)
    return quality

def processImage(scale):
    #get the image
    fileName = input("File name and extension: ")

    #process the image
    pic = os.path.join(sys.path[0], fileName)
    im = Image.open(pic,'r')
    im = ImageOps.mirror(im)
    h,w = im.size       #only time it's flipped - all other references should be opposite of this

    pixel_values = list(im.getdata())
    pixel_positions = []
    for x in range(w):
        #print("row:",y)
        for y in range(h):
            #print("    cell:",x)
            xy = (x*scale,y*scale)
            #print(xy)
            pixel_positions.append(xy)
    print("pixel values and positions done")
    print("Number of pixels:",len(pixel_values))
    h = h*scale
    w = w*scale
    pixels = dict(zip(pixel_positions,pixel_values))
    

    return w,h,pixels,fileName

def colScale(gapSize,palette):

    step1 = palette.get('step 1')
    step2 = palette.get('step 2')
    step3 = palette.get('step 3')
    step4 = palette.get('step 4')
    step5 = palette.get('step 5')
    step6 = palette.get('step 6')
    step7 = palette.get('step 7')

    colours = []

    heatmap =   [
                [0.0, (step1[0]/255, step1[1]/255, step1[2]/255)],
                [0.20, (step2[0]/255, step2[1]/255, step2[2]/255)],
                [0.40, (step3[0]/255, step3[1]/255, step3[2]/255)],
                [0.60, (step4[0]/255, step4[1]/255, step4[2]/255)],
                [0.80, (step5[0]/255, step5[1]/255, step5[2]/255)],
                [0.90, (step6[0]/255, step6[1]/255, step6[2]/255)],
                [1.00, (step7[0]/255, step7[1]/255, step7[2]/255)],
                ]
    
    def gaussian(x, a, b, c, d=0):
        return a * math.exp(-(x - b)**2 / (2 * c**2)) + d

    def pixel(x, width, map=[], spread=1):
        width = float(width)
        r = sum([gaussian(x, p[1][0], p[0] * width, width/(spread*len(map))) for p in map])
        g = sum([gaussian(x, p[1][1], p[0] * width, width/(spread*len(map))) for p in map])
        b = sum([gaussian(x, p[1][2], p[0] * width, width/(spread*len(map))) for p in map])
        #print(min(1.0, r), min(1.0, g), min(1.0, b))
        return min(1.0, r), min(1.0, g), min(1.0, b)
    
    for x in range(0,255,gapSize):
        r, g, b = pixel(x, width=255, map=heatmap)  #float values
        colour = (r,g,b)
        colours.append(colour)
    
    return colours

def saveImage(surface, scriptFile):
    """
    Save surface as PNG with timestamped filename in same folder as script.
    Usage: saveImage(surface, __file__)
    Returns: the full path of the saved file
    """
    import time
    import os
    
    now = time.localtime()
    timestamp = str(now.tm_year) + str(now.tm_mon) + str(now.tm_mday) + str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec)
    fullPath = os.path.realpath(scriptFile) + timestamp + ".png"
    surface.write_to_png(fullPath)
    print("Saved:", fullPath)
    return fullPath