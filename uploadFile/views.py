from django.shortcuts import render
import os
import base64
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

file_poo = os.path.join(settings.FILES_DIR, "test.pdf")
# Save pages in the same folder
testpdf = os.path.join(settings.FILES_DIR, "test.pdf")
page0 = os.path.join(settings.FILES_DIR, "page0.jpg")
CroppedImage = os.path.join(settings.FILES_DIR, "CroppedImage.jpg")
Document011 = os.path.join(settings.FILES_DIR, "Document.011.png")
js = os.path.join(settings.FILES_DIR, "js.png")
getFinal = os.path.join(settings.FILES_DIR, "getFinal.png")
# add tresHold to define image sections

def nextWord(target, source, stringCleaned):
    deleteToFindFor = stringCleaned.split("for:")[1]
    deleteToFindFor = deleteToFindFor.split()

    deleteToFindSubject = stringCleaned.split("Subject:")[1]
    deleteToFindSubject = deleteToFindSubject.split()

    for i, w in enumerate(source):
        if (
            target == "ID:"
            or target == "Date:"
            or target == "Score:"
            or target == "Coverage:"
            or target == "subject.Percentile:"
        ):
            if w == target:
                return source[i + 1]
        elif target == "Subject:":
            subjectTest = []
            for i, w in enumerate(deleteToFindSubject):
                if w == "Remote":
                    return " ".join(subjectTest)[:-1]
                else:
                    subjectTest.append(w)

        elif target == "for:":
            nameTest = []
            for i, w in enumerate(deleteToFindFor):
                if w == "ID:":
                    return " ".join(nameTest)
                else:
                    nameTest.append(w)

        elif target == "Client:":
            if w == target:
                return source[i + 1] + " " + source[i + 2] + " " + source[i + 3]


# Find subject name inside pdf
def findSubjectPracticeFunction(subjectToFind):
    AllSubject = Subject.objects.all()
    print(AllSubject)
    for items in AllSubject:
        itemName = items.nameSubject.lower()
        itemId = items.id
        print(itemName, subjectToFind.lower())
        proximity = fuzz.ratio(itemName, subjectToFind.lower())
        print(proximity)
        if proximity >= 89:
            idSubjectFound = itemId
            return {
                "idSubjectFound": idSubjectFound,
                "itemName": itemName,
            }


def function7():
    try:
        # Get text
        name = []
        pdf = PdfFileReader(testpdf)
        page_1_object = pdf.getPage(0)
        page_1_text = page_1_object.extractText()
        result = page_1_text.split()
       
        # Extract skills from PDF
        skillsPDF = page_1_text.split("StrongSub-Skills")[1]
        skillsPDF = skillsPDF.partition("Work Speed")[0]
        skillsPDF = skillsPDF.split('\n')

        stringCleaned = " ".join(page_1_text.split())

        nameSubject = dict

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
            dataMiner.append(nextWord(dataFile[i], findInside, stringCleaned))
        for i in range(len(dataMiner)):
            if i == 3:
                # get subject from pdf
                nameSubject = findSubjectPracticeFunction(dataMiner[i])
                dataMiner[3] = nameSubject["itemName"]
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
            x, y, w, h = cv2.boundingRect(contour)
            if w > 99:
                dataSkills.append(w)
                print(str(w))

            # if cv2.contourArea(contour) > 1000:
            # dataSkills.append(cv2.contourArea(contour))
            # print(cv2.contourArea(contour))
        # ✅Return to Client
        idSubjectFound = nameSubject["idSubjectFound"]

     
        return Response(
            {
                "scoreBar": dataSkills,
                "name": name,
                "concepts": correctSpillingSkillFromPdf.correctSpilling.findSkillPerCandidateFunction(skillsPDF),
                "dataMiner": dataMiner,
            }
        )
    except Exception:
        return HttpResponse(status=500)


def sortFn(dict):
    # ✅Function Done
    return dict["index"]


def function6():
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
    return function7()


def function5():
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
    return function6()


def documentAnalysis():
    img = cv2.imread(CroppedImage)
    # Output img with window name as 'image'
    # print(img.shape[0])
    # print(img.shape[1])
    img = cv2.resize(img, dsize=(2000, 2200))
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 50, 255, 0)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    cv2.drawContours(img, contours, -1, (255, 255, 255), 2)
    cv2.imwrite(Document011, img)
    # ✅Function Done
    return function5()


class GetAnalysisDocument(APIView):
    def post(self, request):
        os.remove(CroppedImage)
        folder = "virtualStorage/"
        myfile = request.FILES["analysis"]
        fs = FileSystemStorage(location=folder)  # defaults to   MEDIA_ROOT
        fs.save("CroppedImage.jpg", myfile)
        return documentAnalysis()


def function2(currentUserLogged):
    folder = "virtualStorage/"
    fs = FileSystemStorage(location=folder)
    if platform.system() == "Windows":
        pages = convert_from_path(testpdf, 500, poppler_path="./bin")
        for i in range(len(pages)):
            pages[i].save("./virtualStorage/page" + str(i) + ".jpg", "JPEG")
    else:
        default_path = os.path.join(settings.NEW_NAME_PDF)
        # print(testpdf, default_path)
        pages = convert_from_path(testpdf, 500)
        # print("pages", pages)
        for i in range(len(pages)):
            pages[i].save("./virtualStorage/page" + str(i) + ".jpg", "JPEG")
    # ✅Function Done
    with open(page0, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    return HttpResponse(image_data, content_type="image/jpg")


def createImages(filename, currentUserLogged):
    os.remove(file_poo)
    file_path = os.path.join(settings.FILES_DIR, filename)
    # default_path = os.path.join(settings.NEW_NAME_PDF)

    os.rename(file_path, testpdf)
    return function2(currentUserLogged)

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
                return createImages(myfile.name, currentUserLogged)
        except Exception:
            return HttpResponse(status=500)

    def get(self, request):
        return Response({"message": "request done"})
