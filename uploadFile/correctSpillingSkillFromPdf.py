from .models import SubjectSkills,Subject
from rapidfuzz import fuzz

def sortFn(dict):
    #✅Function Done
    return dict['index']

def seed(deleteToFindFor):
    skillTest = []
    for i, w in enumerate(deleteToFindFor):
        if w == "Speed/Accuracy":
            return "".join(skillTest)
        else:
            skillTest.append(w)

def correctSpillingJAVAPractice(allSkills,stringCleaned, stringCleanedTest):


    deleteToFindFor =  stringCleanedTest.split("StrongSub-Skills")[1]
    deleteToFindFor = deleteToFindFor.split()

    foo = seed(deleteToFindFor).lower()
   
    skillOrderHightToLow = []
    findLabel = str()
    
    for items in allSkills:
  
        joinWord = items.nameSubSkill.split()
        findLabel = "".join(joinWord)
        order =  foo.find(findLabel)
        if not order == -1:
            skillOrderHightToLow.append({"index": order, "value": items.nameSubSkill})

    skillOrderHightToLow.sort(key=sortFn)
    skillOrderHightToLow.reverse()
  
    return skillOrderHightToLow

class correctSpilling:
    def findSkillPerCandidateFunction(subjectIdToFindEverySkill,stringCleaned):

        allSkills = SubjectSkills.objects.filter(subjectId=subjectIdToFindEverySkill)
       
        subject = Subject.objects.get(id=subjectIdToFindEverySkill)

        stringCleanedTest =stringCleaned

        stringCleaned =stringCleaned.lower()

        
        #if(subject.nameSubject == 'mdc basic java interview 2'):
        return correctSpillingJAVAPractice(allSkills,stringCleaned, stringCleanedTest)
        


 
     