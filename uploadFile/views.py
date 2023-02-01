from django.shortcuts import render
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import FileSystemStorage

import platform
import numpy as np
import cv2
from rapidfuzz import fuzz
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader


from django.conf import settings
from .models import (
    Subject,
)

from uploadFile import correctSpillingSkillFromPdf
from uploadFile import circleGraphFunction
from uploadFile import footerLabelGraph

# Save pages in the same folder
testpdf = os.path.join(settings.FILES_DIR, "test.pdf")
page0 = os.path.join(settings.FILES_DIR, "page0.jpg")
CroppedImage = os.path.join(settings.FILES_DIR, "CroppedImage.jpg")
Document011 = os.path.join(settings.FILES_DIR, "Document.011.png")
js = os.path.join(settings.FILES_DIR, "js.png")
getFinal = os.path.join(settings.FILES_DIR, "getFinal.png")

# 🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧 Footer Graphs 🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧🚧
CroppedImageFooterCircle = os.path.join(
    settings.FILES_DIR, "CroppedImageFooterCircle.jpg"
)
CroppedLevelUpRow1 = os.path.join(settings.FILES_DIR, "CroppedLevelUpRow1.jpg")
CroppedLevelUpRow2 = os.path.join(settings.FILES_DIR, "CroppedLevelUpRow2.jpg")
CroppedLevelUpRow1Blackest = os.path.join(
    settings.FILES_DIR, "CroppedLevelUpRow1Blackest.jpg"
)
# pytorch
AreaG = os.path.join(settings.FILES_DIR, "AreaG.jpg")
# add tresHold to define image sections


def deleteBlur(imageBlur):
    # DELETE BLUR
    img = cv2.imread(imageBlur)
    Z = img.reshape((-1, 3))

    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 8
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))
    cv2.imwrite(imageBlur, res2)


def nextWord(target, source):
    for i, w in enumerate(source):
        if ( target == "ID:" or target == "Date:" or target == "Score:" or target == "Coverage:" or target == "subject.Percentile:"):
            if w == target:
                return source[i + 1]
        elif target == "Subject:":
            if w == target:
                return ( source[i + 1] + source[i + 2] + source[i + 3] + source[i + 4] + source[i + 5] + source[i + 6] + source[i + 7])
        elif target == "for:":
            if w == target:
                return source[i + 1] + " " + source[i + 2]
        elif target == "Client:":
            if w == target:
                return source[i + 1] + " " + source[i + 2] + " " + source[i + 3]


# Find subject name inside pdf
idSubjectFound = int()


def findSubjectPracticeFunction(subjectToFind):
    AllSubject = Subject.objects.all()
    for items in AllSubject:
        itemName = items.nameSubject.lower()
        itemId = items.id
        print(itemName, subjectToFind.lower())
        proximity = fuzz.ratio(itemName, subjectToFind.lower())
        print(proximity)
        if proximity >= 80:
            global idSubjectFound
            idSubjectFound = itemId
            return itemName


def function7(currentUserLogged):
    try:
        # Get text
        name = []
        pdf = PdfFileReader(testpdf)
        page_1_object = pdf.getPage(0)
        page_1_text = page_1_object.extractText()
        result = page_1_text.split()
        stringCleaned = " ".join(page_1_text.split())

        name.append(result[6] + " " + result[7])
        # print(page_1_text.split(), sep='\n')

        findInside = stringCleaned.split()
        dataFile = [
            "for:",
            "ID:",
            "Date:",
            "Subject:",
            "Client:",
            "Score:",
            "subject.Percentile:",
            "Coverage:",
        ]
        dataMiner = []

        for i in range(len(dataFile)):
            dataMiner.append(nextWord(dataFile[i], findInside))
        for i in range(len(dataMiner)):
            if i == 3:
                # get subject from pdf
                dataMiner[3] = findSubjectPracticeFunction(dataMiner[i])
        for i in range(len(dataMiner)):
            if i == 0:
                dataMiner[i] = {
                    "label": "Assessment Result for",
                    "subjectName": dataMiner[i],
                }
            if i == 1:
                dataMiner[i] = {"label": "ID", "subjectId": dataMiner[i]}
            if i == 2:
                dataMiner[i] = {"label": "Date", "subjectDate": dataMiner[i]}
            if i == 3:
                dataMiner[i] = {
                    "label": "Subject",
                    "subjectInterViewName": dataMiner[i],
                }
            if i == 4:
                dataMiner[i] = {"label": "Client", "subjectClient": dataMiner[i]}
            if i == 5:
                dataMiner[i] = {"label": "Score", "subjectScore": dataMiner[i]}
            if i == 6:
                deletePercentile = dataMiner[i]
                dataMiner[i] = {
                    "label": "Percentile",
                    "subjectPercentile": deletePercentile.replace("%", ""),
                }
            if i == 7:
                deletePercentile = dataMiner[i]
                dataMiner[i] = {
                    "label": "SubjectCoverage",
                    "subjectSubjectCoverage": deletePercentile.replace("%", ""),
                }

        # print(findSkillPerCandidateFunction(idSubjectFound,stringCleaned))

        # Bar Graph by skill result
        dataSkills = []
        image = cv2.imread(getFinal)
        deep_copy = image.copy()

        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(image_gray, 210, 255, cv2.THRESH_BINARY)
        thresh = 255 - thresh

        shapes, hierarchy = cv2.findContours(
            image=thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE
        )
        cv2.drawContours(
            image=deep_copy,
            contours=shapes,
            contourIdx=-1,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.LINE_AA,
        )
        for contour in shapes:
            if cv2.contourArea(contour) > 1000:
                dataSkills.append(cv2.contourArea(contour))
                # print(cv2.contourArea(contour))

        # footer
        listDataLevelUp = []
        listDataLevelUp.append(
            footerLabelGraph.footerPDF.FooterRowLevelUp(
                CroppedLevelUpRow1, "Work Speed/Accuracy"
            )
        )
        listDataLevelUp.append(
            footerLabelGraph.footerPDF.FooterRowLevelUp(
                CroppedLevelUpRow2, "Application Ability"
            )
        )

        # ✅Return to Client
        print(idSubjectFound)
        return Response(
            {
                "scoreBar": dataSkills,
                "name": name,
                "concepts": correctSpillingSkillFromPdf.correctSpilling.findSkillPerCandidateFunction(
                    idSubjectFound, stringCleaned
                ),
                "subjectCoverage": circleGraphFunction.pieChart.CircleCV(),
                "FooterLevel": listDataLevelUp,
                "dataMiner": dataMiner,
            }
        )
    except Exception:
        return HttpResponse(status=500)


def sortFn(dict):
    # ✅Function Done
    return dict["index"]


def function6(currentUserLogged):

    image = cv2.imread(js)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 1))
    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2
    )
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)

    # Remove vertical
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2
    )
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)

    cv2.imwrite(getFinal, image)
    # ✅Function Done
    return function7(currentUserLogged)


def function5(currentUserLogged):
    image = cv2.imread(Document011)
    msk = image.copy()
    msk = cv2.medianBlur(msk, 25)
    msk = cv2.erode(msk, np.ones((7, 7)))
    msk = cv2.threshold(msk, 200, 255, cv2.THRESH_BINARY)[1]
    msk = cv2.GaussianBlur(msk, (5, 0), 25)
    msk = cv2.threshold(msk, 120, 255, cv2.THRESH_BINARY)[1]
    msk = cv2.erode(msk, np.ones((31, 31)))
    image[np.where(msk != 0)] = 255
    cv2.imwrite(js, image)
    # ✅Function Done
    return function6(currentUserLogged)


def function4(currentUserLogged):
    img = cv2.imread(CroppedImage)
    # Output img with window name as 'image'

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 50, 255, 0)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    cv2.drawContours(img, contours, -1, (255, 255, 255), 2)

    cv2.imwrite(Document011, img)

    # DELETE BLUR ✅
    # deleteBlur(CroppedImageFooterCircle)
    deleteBlur(AreaG)
    # ✅Function Done
    return function5(currentUserLogged)


def function3(currentUserLogged):
    try:
        img = cv2.imread(page0)
        # Cropping an image
        # cropped_image = img[2050:3300, 850:2900]
        cropped_image = img[2050:3300, 1540:2900]
        # Save the cropped image
        cv2.imwrite(CroppedImage, cropped_image)

        # footer Graphs
        cropped_image_footer = img[3580:4400, 2600:3500]
        cv2.imwrite(CroppedImageFooterCircle, cropped_image_footer)

        # (arriba:abajo,derecha:izquierda)
        # cropped_image_foteer = img[3500:4500, 1500:3000], bar cropped_image_foteerLevelUp1 = img[3500:4400, 1000:2500]
        cropped_image_foteerLevelUp1 = img[3510:3720, 250:2050]
        cv2.imwrite(CroppedLevelUpRow1, cropped_image_foteerLevelUp1)

        cropped_image_foteerLevelUp2 = img[4120:4400, 250:2050]
        cv2.imwrite(CroppedLevelUpRow2, cropped_image_foteerLevelUp2)
        # ✅Function Done

        # py AreaG
        cropped_image_footerArea = img[3500:3600, 2500:3650]
        cv2.imwrite(AreaG, cropped_image_footerArea)
        return function4(currentUserLogged)
    except Exception:
        return {"message": "There was an error uploading the file"}

############################

def function2(currentUserLogged):
    folder = "virtualStorage/"
    fs = FileSystemStorage(location=folder)
    if platform.system() == "Windows":
        pages = convert_from_path(testpdf, 500, poppler_path="./bin")
        for i in range(len(pages)):
            pages[i].save("./virtualStorage/page" + str(i) + ".jpg", "JPEG")
    else:
        default_path = os.path.join(settings.NEW_NAME_PDF)
        print(testpdf, default_path)

        pages = convert_from_path(testpdf, 500)
        print("pages", pages)
        for i in range(len(pages)):
            pages[i].save("./virtualStorage/page" + str(i) + ".jpg", "JPEG")
    # ✅Function Done
    return function3(currentUserLogged)


###############################

file_poo = os.path.join(settings.FILES_DIR, "test.pdf")

def documentAnalysis(filename, currentUserLogged):
    os.remove(file_poo)
    file_path = os.path.join(settings.FILES_DIR, filename)
    # default_path = os.path.join(settings.NEW_NAME_PDF)

    os.rename(file_path, testpdf)
    return function2(currentUserLogged)
    """ os.rename(file_path,"./virtualStorage/test.pdf") """

class UploadDocument(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        try:
            currentUserLogged = request.user
            folder = "virtualStorage/"
            if request.method == "POST" and request.FILES["upload"]:
                myfile = request.FILES["upload"]
                fs = FileSystemStorage(location=folder)  # defaults to   MEDIA_ROOT
                fs.save(myfile.name, myfile)
                return documentAnalysis(myfile.name, currentUserLogged)
        except Exception:
            return HttpResponse(status=500)

    def get(self, request):
        return Response({"message": "request done"})
#############################################################################################