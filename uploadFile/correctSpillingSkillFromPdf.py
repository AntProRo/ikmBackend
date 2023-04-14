from .models import SubjectSkills,Subject
from rapidfuzz import fuzz

def sortFn(dict):
    #✅Function Done
    return dict['index']

class correctSpilling:
    def findSkillPerCandidateFunction(skillsPDF):
        data=skillsPDF[::-1]
        data= data[1:-1]

        result =[]
        for i,item in enumerate(data):
            result.append({"index":i,"value":item.lower()})
        return result