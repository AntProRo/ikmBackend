from django.urls import path
from recruiter_options import views

urlpatterns = [
    #Create data
    path('createPractice/', views.CreatePractice.as_view(), name='savePractice'),
    path('createSubject/<int:id>/',views.CreateSubject.as_view(),name='saveSubject'),
    path('createSkills/<int:id>/',views.CreateSkill.as_view(),name='saveSkills'),
    #save candidates data fromPDF and get all data saved 
    path('processFile/', views.processData.as_view(), name='save'),
    #Get all Practices, Subjects and Skills
    path('getAllSubject/',views.GetAllSubjectsAndPractices.as_view(),name='getAllSavedSubject'),
    path('getAllSkillsBySubject/<int:id>/',views.GetSkillsBySubject.as_view(),name='getSkills'),
    #Update data
    path('updatePractice/<int:id>/',views.UpdatePractice.as_view(),name='updatePracticeByID'),
    path('updateSubject/<int:id>/',views.UpdateSubject.as_view(),name='updateSubjectByID'),
    path('updateSkill/<int:id>/',views.UpdateSkill.as_view(),name='updateSkillByID'),
    #Delete data
    path('deleteCandidate/<int:id>/',views.DeleteCandidate.as_view(),name='deleteCandidateByID'),
    path('deletePractice/<int:id>/',views.DeletePractice.as_view(),name='deletePracticeById'),
    path('deleteSubject/<int:id>/',views.DeleteSubject.as_view(),name='deleteSubjectById'),
    path('deleteSkill/<int:id>/',views.DeleteSkill.as_view(),name='deleteSkillByID'),
    #CROP options
    path('saveCrop/', views.DefaultCropOptions.as_view(), name='DefaultCropOptions'),
]