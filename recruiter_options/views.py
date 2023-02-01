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
    # Get data
    def get (self,request):
            data = Candidate.objects.filter(recruiter=request.user)
            
            d = data.all().select_related('SubjectUserAccount')

            #f = Score.objects.all().select_related('subjectSkillId','score')
            result= []
            

            for i in d:
                #i.SubjectUserAccount.all().select_related('SubjectUserAccount')
                #print(i.SubjectUserAccount.nameSubject )
                #print(i.SubjectUserAccount.practiceId.namePractice )
        
            
                scoreCandidate = Score.objects.filter(candidateId = i.id).select_related('subjectSkillId')
                coverageCandidate = SubjectCoverage.objects.get(candidateId = i.id) 
                #print(i.SubjectUserAccount.nameSubject)
                result.append({"profileData":i ,"scoreData":scoreCandidate,"subjectCoverage":coverageCandidate})

            data = []
         
            
            for i in range(len(result)):
            
                
                skill =[]
                stringToDate =result[i]["profileData"].date
                createdAt = result[i]["profileData"].created_at
                updatedAt = result[i]["profileData"].updated_at
                
                userData = {"SubjectUserAccount":result[i]["profileData"].SubjectUserAccount.id,
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

                userCoverage = {"weak":result[i]["subjectCoverage"].weak,
                    "proficient":result[i]["subjectCoverage"].proficient, 
                    "strong":result[i]["subjectCoverage"].strong,
                    "workSpeedAccuracy":result[i]["subjectCoverage"].workSpeedAccuracy,
                    "applicationAbility":result[i]["subjectCoverage"].applicationAbility
                    }

                
                #print(i["profileData"].nameCandidate)
                #print(i["profileData"].SubjectUserAccount.nameSubject,i["profileData"].SubjectUserAccount.id )
                #print(i["profileData"].SubjectUserAccount.practiceId.namePractice,i["profileData"].SubjectUserAccount.practiceId.id )
                for j in result[i]["scoreData"]:
                    skill.append({"idSkill":j.subjectSkillId.id,"nameSkill":j.subjectSkillId.nameSubSkill,"score":j.score}),
                    #print(j.score,j.subjectSkillId.nameSubSkill,j.subjectSkillId.id)

                data.append({"userData":userData, "userSkillScore":skill, "userCoverage":userCoverage})
                    
      
                     
                #print(i["subjectCoverage"].weak,i["subjectCoverage"].workSpeedAccuracy)
         
        
            foo = json.dumps(data)
            return HttpResponse(foo)
  

        #save document
    def post(self, request):
        current_user = request.user
        # print (current_user.id)

        body = json.loads(request.body)
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

        for i in allSkills:
            allSkillsFound.append({i.nameSubSkill: i.id})

        for key, value in candidateSkills.items():
            str1 = key.lower()
            for key in allSkillsFound:
                if str1 in key:
                    print(str1, key[str1])
                    score = Score()
                    score.subjectSkillId = SubjectSkills.objects.get(id=int(key[str1]))
                    score.score = value
                    score.candidateId = Candidate.objects.get(id=candidate.id)
                    score.save()
        # save rest data
        coverage = SubjectCoverage()
        coverage.workSpeedAccuracy = body["workSpeedAccuracy"]
        coverage.applicationAbility = body["applicationAbility"]
        coverage.weak = body["circleBar"]["weak"] 
        coverage.proficient = body["circleBar"]["proficient"] 
        coverage.strong = body["circleBar"]["strong"] 
        coverage.candidateId = Candidate.objects.get(id=candidate.id)
        coverage.save()

        return Response({"message": "Document saved"})
# user logged Controller


class PracticeControllers(APIView):

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

class DeletePractice(APIView):
    def delete(self,request,id):
        get_object_or_404(Practice, id=id)
        print(id)
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



class SubjectController(APIView):
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


class SkillController(APIView):
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

class getSkillsBySubject(APIView):
    def get(self,request,id):
        get_object_or_404(Subject, id=id)
        allSubjectsRelations = SubjectSkills.objects.filter(subjectId=id)
        result = []
        for i in allSubjectsRelations:
            result.append({"name":i.nameSubSkill,"id":i.id})
        result = json.dumps(result)
        print(result)

        return HttpResponse(result)
        
            # your logic here
        return HttpResponse(status=500)

