from django.conf import settings
import cv2
import os

CroppedLevelUpRow1Blackest = os.path.join(settings.FILES_DIR,"CroppedLevelUpRow1Blackest.jpg")

class footerPDF:
    def FooterRowLevelUp(image,context):
        try:
            label =str("")
            
            img = cv2.imread(image)
            # convert the image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # apply thresholding to convert the grayscale image to a binary image
            ret,thresh = cv2.threshold(gray,50,255,0)

            # find the contours
            contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            if(context == "Work Speed/Accuracy"):
            
                if len(contours) == 99 or len(contours) == 100:
                    label="Above Average"
                elif len(contours) == 90 or len(contours) == 91:
                    label ="Average"
                elif len(contours) == 89 or len(contours) == 90:
                    label = "Very Slow"
                elif len(contours) == 93 or len(contours) == 94:
                    label = "Very Fast"
                elif len(contours) == 101 or len(contours) == 102:
                    label = "Below Average"
            elif(context == "Application Ability"):
                cv2.imwrite(CroppedLevelUpRow1Blackest, thresh)
                if len(contours) == 97:
                    label="Significant"
                elif len(contours) == 96:
                    label ="Moderate"
                elif len(contours) == 89:
                    label = "Negligible"
                elif len(contours) >= 98:
                    label = "Extensive"
                elif len(contours) == 90:
                    label = "Limited"
            #✅Function Done
            return {"value":label,"context":context}
        except Exception:
                return ({"message": "There was an error FooterRowLevelUp function"})