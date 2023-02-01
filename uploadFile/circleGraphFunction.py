from django.conf import settings
import cv2
import os
import numpy as np
import math

CroppedImageFooterCircle = os.path.join(settings.FILES_DIR,"CroppedImageFooterCircle.jpg")
# Round values
def truncate(n, decimals = 0): 
    multiplier = 10 ** decimals 
    return int(n * multiplier) / multiplier #✅

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def colorArea(area,image,color):
    _, binary = cv2.threshold(area, 225, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # draw all contours
    image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
        
    for i in contours[1:]:
        if truncate(cv2.contourArea(i), -4) > 1:#✅
        #detect area ✅
        #return {"color":color,"value":truncate(cv2.contourArea(i), -4)}#
            return {"color":color,"value":cv2.contourArea(i)}#✅

class pieChart:
    #Circle get color
    def CircleCV():
        # Read the images
        img = cv2.imread(CroppedImageFooterCircle)
        
        # Resizing the image
        image = cv2.resize(img, (700, 600))
        
        # Convert Image to Image HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        #maskTofindColorsArea = ["green","red","yellow"]
        #green
        # Defining lower and upper bound HSV values
        lowerGreen = np.array([50, 100, 100])
        upperGreen = np.array([70, 255, 255])
        # Defining mask for detecting color
        maskGreen = cv2.inRange(hsv, lowerGreen, upperGreen)

        #Red
        lowerRed= np.array([170, 160, 70])
        upperRed = np.array([180, 250, 250])
        maskRed = cv2.inRange(hsv, lowerRed, upperRed)
        #cv2.imshow("Red", maskRed)

        #yellow
        lowerYellow= np.array([18, 40, 90])
        upperYellow = np.array([27, 255, 255])
        maskYellow = cv2.inRange(hsv, lowerYellow, upperYellow)
        #cv2.imshow("Yellow", maskYellow)

        listArea = []

        listArea.append(colorArea(maskRed,image,"Weak"))#✅
        listArea.append(colorArea(maskYellow,image,"Proficient"))#✅
        

        flag = not np.any(maskGreen)
        if flag:
            listArea.append({"color":"Strong","value":0})
        else:
            listArea.append(colorArea(maskGreen,image,"Strong"))
        #✅
        total = 0
        for i in range(len(listArea)):
            total = total +listArea[i]["value"]
        
        newListArea=[]
        for i in range(len(listArea)):
            

            if(listArea[i]["color"] =="Proficient"):
                result = {"color":"Proficient","value":truncate((listArea[i]["value"] / total) * 100) -1}
                newListArea.append(result)
            
            if(listArea[i]["color"] =="Weak"):
                result = {"color":"Weak","value":round_up((listArea[i]["value"] / total) * 100)}
                newListArea.append(result)
                
        
            if(listArea[i]["color"] =="Strong"):
                result = {"color":"Strong","value":round_up((listArea[i]["value"] / total) * 100)}
                newListArea.append(result)
        
    
        
        flag= 0
        for i in range(len(newListArea)):
            if(newListArea[i]["color"] =="Strong" and newListArea[i]["value"] == 0.0):
                flag = 1
        for i in range(len(newListArea)):
            if(newListArea[i]["color"] =="Proficient" and flag == 1):
                newListArea[i]["value"] = newListArea[i]["value"] +1
        
        
        #print(newListArea)
        return newListArea   
        # Make python sleep for unlimited time
