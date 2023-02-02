from .models import SubjectSkills,Subject

def sortFn(dict):
    #✅Function Done
    return dict['index']

def correctSpillingJAVAPractice(allSkills,stringCleaned):
    skillOrderHightToLow = []
    findLabel = str()
    
    for items in allSkills:
        if items.nameSubSkill == 'rest web services':
            findLabel = "rest w eb services"
        elif items.nameSubSkill == 'spring boot testing':
            findLabel = "spring boot t esting"
        else:
            findLabel = items.nameSubSkill
    
        order =  stringCleaned.find(findLabel)
        if not order == -1:
            skillOrderHightToLow.append({"index": order, "value": items.nameSubSkill})

    skillOrderHightToLow.sort(key=sortFn)
    skillOrderHightToLow.reverse()
  
    return skillOrderHightToLow

class correctSpilling:
    def findSkillPerCandidateFunction(subjectIdToFindEverySkill,stringCleaned):

        allSkills = SubjectSkills.objects.filter(subjectId=subjectIdToFindEverySkill)
       
        subject = Subject.objects.get(id=subjectIdToFindEverySkill)
        stringCleaned =stringCleaned.lower()

       
        if(subject.nameSubject == 'mdc basic java interview 2'):
            return correctSpillingJAVAPractice(allSkills,stringCleaned)


 
     