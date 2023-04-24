from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from datetime import date
from django.utils.dateparse import parse_datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404,JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.core import serializers

from django.core.serializers.json import DjangoJSONEncoder

from uploadFile.models import (
    UserAccount,
    Candidate,
    Practice,
    Subject,
    SubjectSkills,
    Score,
    SubjectCoverage,
)
# Create your views here.
# Global data#
idCandidate = object()
class processData(APIView):
    permission_classes = [
    IsAuthenticated,
]
    # Get all users data
    def get(self,request):
            data = Candidate.objects.filter(recruiter=request.user)
            d = data.all().select_related('SubjectUserAccount')
            result= []
            for i in d:
                scoreCandidate = Score.objects.filter(candidateId = i.id).select_related('subjectSkillId')
                result.append({"profileData":i ,"scoreData":scoreCandidate,})

            data = []
            for i in range(len(result)):
                skill =[]
                stringToDate =result[i]["profileData"].date
                createdAt = result[i]["profileData"].created_at
                updatedAt = result[i]["profileData"].updated_at
                
                userData = {"id":result[i]["profileData"].id,
                    "SubjectUserAccount":result[i]["profileData"].SubjectUserAccount.id,
                    "bullHornId":result[i]["profileData"].bullHornId,
                    "nameCandidate":result[i]["profileData"].nameCandidate,
                    "date": stringToDate.strftime("%m/%d/%Y") ,
                    "subjectName":result[i]["profileData"].SubjectUserAccount.nameSubject,
                    "scoreAssessmentTotal":result[i]["profileData"].scoreAssessmentTotal,
                    "client":result[i]["profileData"].client,
                    "percentile":result[i]["profileData"].percentile,
                    "subjectCoverageTotal":result[i]["profileData"].subjectCoverageTotal,
                    "createdAt":createdAt.strftime("%m/%d/%Y"),
                    "updatedAt": updatedAt.strftime("%m/%d/%Y"),

                    "practiceId":result[i]["profileData"].SubjectUserAccount.practiceId.id}
                for j in result[i]["scoreData"]:
                    skill.append({"idSkill":j.subjectSkillId.id,"nameSkill":j.subjectSkillId.nameSubSkill,"score":j.score}),
                    #print(j.score,j.subjectSkillId.nameSubSkill,j.subjectSkillId.id)

                data.append({"userData":userData, "userSkillScore":skill})
            foo = json.dumps(data)
            return HttpResponse(foo)

        #save document information
    def post(self, request):
        current_user = request.user
        # print (current_user.id)
        body = json.loads(request.body)
        print(body)
        # get date parse
        candidateDate = parse_datetime(body["date"])
        # get id of subject
        getSubjectId = Subject.objects.get(
            nameSubject=body["subjectName"].lower()
        )
        allSkills = SubjectSkills.objects.filter(subjectId=getSubjectId)

        candidate = Candidate()
        candidate.recruiter = current_user
        candidate.nameCandidate = body["nameCandidate"]
        candidate.date = candidateDate
        candidate.bullHornId = int(body["bullHornId"])
        candidate.subjectName = body["subjectName"].lower()
        candidate.scoreAssessmentTotal = int(body["scoreAssessmentTotal"])
        candidate.client = body["client"]
        candidate.percentile = int(body["percentile"])
        candidate.subjectCoverageTotal = int(body["subjectCoverageTotal"])
        candidate.SubjectUserAccount = getSubjectId
        candidate.save()

        #save Skills
        candidateSkills = body["skills"]
        allSkillsFound = []

        def JoinWordsToMatchSkillDataBase(word):
            word = word.lower().split()
            return "".join(word)

        for i in allSkills:
            findLabel = JoinWordsToMatchSkillDataBase(i.nameSubSkill)
            allSkillsFound.append({findLabel: i.id})

        for key, value in candidateSkills.items():
            str1 = JoinWordsToMatchSkillDataBase(key)
            for key in allSkillsFound:
                if str1 in key :
                    #print("save",str1, key[str1])
                    score = Score()
                    score.subjectSkillId = SubjectSkills.objects.get(id=int(key[str1]))
                    score.score = value
                    score.candidateId = Candidate.objects.get(id=candidate.id)
                    score.save()

        return Response({"message": "Document saved"})
# user logged Controller

class DeleteCandidate(APIView):
    def delete(self,request,id):
        get_object_or_404(Candidate,id=id)
        findCandidate = Candidate.objects.get(id=id)
        findCandidate.delete()
        return Response({"message": "Candidate Deleted"})
#PRACTICE
class CreatePractice(APIView):
    def post(self, request):
        body = json.loads(request.body)

        if not Practice.objects.filter(
            namePractice=body["namePractice"].lower()
        ).exists():
            practice = Practice()
            practice.recruiterId = request.user
            practice.namePractice = body["namePractice"].lower()
            practice.save()
            return Response({"message": "practice saved"})
        else:
            # your logic here
            return HttpResponse(status=500)
        
class UpdatePractice(APIView):
    def put(self,request,id):
        body = json.loads(request.body)
        findPractice = Practice.objects.get(id=id)
        if  not Practice.objects.filter(
            namePractice=body["namePractice"].lower()
        ).exists():
            findPractice.namePractice = body["namePractice"].lower()
            findPractice.save()
            return Response({"message": "Practice updated"})
        else:
            # your logic here
            return HttpResponse(status=500)


class DeletePractice(APIView):
    def delete(self,request,id):
        get_object_or_404(Practice, id=id)
        findPractice = Practice.objects.get(id=id)
        findPractice.delete()
        return Response({"message": "Practice deleted"})



class GetAllSubjectsAndPractices(APIView):
    def get(self,request):
        allUserPractice = Practice.objects.filter(recruiterId = request.user)
        #listPractice = []
        listSubject = []
        for i in allUserPractice:
            found = Subject.objects.filter(practiceId=i.id)
            #data = found.values("nameSubject","id")
            #data = json.dumps(list(data), cls=DjangoJSONEncoder)
            data = serializers.serialize('json', list(found), fields=("nameSubject","id"))
          
            listSubject.append({"idPractice":i.id, "namePractice":i.namePractice,"subjectList":json.loads(data)})
         
            #listPractice.append({"idPractice":i.id,"namePractice":i.namePractice}
        result = listSubject
        return JsonResponse(result,safe=False)

class CreateSubject(APIView):
    def post(self, request, id):
        findPracticeId = get_object_or_404(Practice, id=id)
        body = json.loads(request.body)

        if  not Subject.objects.filter(
            nameSubject=body["nameSubject"].lower(),  practiceId =id
        ).exists():
            subject = Subject()
            subject.practiceId = findPracticeId
            subject.nameSubject = body["nameSubject"].lower()
            subject.save()
            return Response({"message": "subject saved"})
        else:
            # your logic here
            return HttpResponse(status=500)
class UpdateSubject(APIView):        
    def put(self,request,id):
        findPracticeId = get_object_or_404(Practice, id=id)
        body = json.loads(request.body)
      
        findSubject = Subject.objects.get(id=body["idSubject"])
        if  not Subject.objects.filter(
            nameSubject=body["nameSubject"].lower(), practiceId =id
        ).exists():
            findSubject.practiceId = findPracticeId
            findSubject.nameSubject = body["nameSubject"].lower()
            findSubject.save()
            return Response({"message": "subject updated"})
        else:
            # your logic here
            return HttpResponse(status=500)
        
class DeleteSubject(APIView):       
    def delete(self,request,id):
        get_object_or_404(Subject, id=id)
        findSubject = Subject.objects.get(id=id)
        findSubject.delete()
        return Response({"message": "Subject deleted"})

#SKILLS
class GetSkillsBySubject(APIView):
    def get(self,request,id):
        get_object_or_404(Subject, id=id)
        allSubjectsRelations = SubjectSkills.objects.filter(subjectId=id)
        result = []
        for i in allSubjectsRelations:
            result.append({"name":i.nameSubSkill,"id":i.id})
        result = json.dumps(result)
        print(result)

        return HttpResponse(result)
    
class CreateSkill(APIView):
    def post(self, request, id):
        body = json.loads(request.body)
        findSubjectId = get_object_or_404(Subject, id=id)

        if not SubjectSkills.objects.filter(
            nameSubSkill=body["nameSubSkill"].lower() ,subjectId =id
        ).exists():
            skill = SubjectSkills()
            skill.subjectId = findSubjectId
            skill.nameSubSkill = body["nameSubSkill"].lower()
            skill.save()
            return Response({"message": "skill saved"})
        else:
            # your logic here
            return HttpResponse(status=500)

class UpdateSkill(APIView):
    def put(self, request,id):
        body = json.loads(request.body)
        #verify if subject exist
        findSubject = get_object_or_404(Subject,id=id)
        #find skill by the id skill and subject id
        findSkill = SubjectSkills.objects.get(id= body["idSkill"],subjectId= id)
        #verify if current nameSkill and idSubject are already created
        if  not SubjectSkills.objects.filter(
           nameSubSkill = body["nameSubSkill"].lower(), subjectId= id
        ).exists():
            findSkill.subjectId = findSubject
            findSkill.nameSubSkill = body["nameSubSkill"].lower()
            findSkill.save()
            return Response({"message": "Skill updated"})
        else:
            # your logic here
            return HttpResponse(status=500)
        
class DeleteSkill(APIView):
    def delete(self,request,id):
        get_object_or_404(SubjectSkills,id=id)
        findSkill = SubjectSkills.objects.get(id=id)
        findSkill.delete()
        return Response({"message": "Skill Deleted"})


#Crop options
class DefaultCropOptions(APIView):
    def put(self,request):
        current_user = request.user
        body = json.loads(request.body)
        updateCropDefault = UserAccount.objects.get(id = current_user.id)
        updateCropDefault.height = float(body["height"])
        updateCropDefault.unit= body["unit"]
        updateCropDefault.width = float(body["width"])
        updateCropDefault.x = float(body["x"])
        updateCropDefault.y = float(body["y"])
        updateCropDefault.save()
        return Response({"message": "Crop default saved"})

    def get(self,request):
        result = {
            "height":request.user.height, 
            "width":request.user.width,
            "unit":request.user.unit,
            "x":request.user.x,
            "y":request.user.y,
            }
        result= json.dumps(result)
        return HttpResponse(result)



      

   
       