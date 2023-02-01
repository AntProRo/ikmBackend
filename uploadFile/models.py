from django.db import models
from accounts.models import UserAccount
# Create your models here.
# example one to one 
#recruiter = models.OneToOneField(UserAccount, on_delete=models.CASCADE,null=False, blank= False)

#one to many ( User account can have multiples candidates, but candidates can have one recruiter)
 ## 🚧🚧🚧🚧🚧🚧🚧🚧🚧
class Practice(models.Model):
    recruiterId = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, blank= False)
    namePractice = models.CharField(max_length =100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Subject(models.Model):
    practiceId = models.ForeignKey(Practice, on_delete=models.CASCADE, null=False, blank= False)
    nameSubject = models.CharField(max_length =200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Candidate(models.Model):
    recruiter = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, blank= False)
    SubjectUserAccount = models.ForeignKey(Subject, on_delete=models.CASCADE, null=False, blank=False)
    bullHornId = models.FloatField(null=True)
    nameCandidate = models.CharField(max_length =100)
    date = models.DateField()
    subjectName = models.CharField(max_length =100)
    scoreAssessmentTotal = models.FloatField(null=True)
    client = models.CharField(max_length =100)
    percentile = models.FloatField()
    subjectCoverageTotal = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # django create the relation with user account


class SubjectSkills(models.Model):
    #one to one this score belongs to score
    subjectId = models.ForeignKey(Subject, on_delete=models.CASCADE, null=False, blank= False)
    nameSubSkill = models.CharField(max_length =100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Score(models.Model):
    #one to one this score belongs to candidate
    candidateId = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=False, blank= False)
    subjectSkillId = models.ForeignKey(SubjectSkills, on_delete=models.CASCADE, null=False, blank= False)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SubjectCoverage(models.Model):
    candidateId = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=False, blank= False)
    weak= models.IntegerField()
    proficient = models.IntegerField()
    strong= models.IntegerField()
    workSpeedAccuracy = models.CharField(max_length =100)
    applicationAbility = models.CharField(max_length =100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




## 🚧🚧🚧🚧🚧🚧🚧🚧🚧
#many to many ( One score can have multiples skills and skills can have multiples score 