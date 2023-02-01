from django.urls import path
from recruiter_options import views

urlpatterns = [
    path('processFile/', views.processData.as_view(), name='save'),
    path('createPractice/', views.PracticeControllers.as_view(), name='savePractice'),
    path('createSubject/<int:id>/',views.SubjectController.as_view(),name='saveSubject'),
    path('getAllSubject/',views.GetAllSubjectsAndPractices.as_view(),name='getAllSavedSubject'),
    path('createSkills/<int:id>/',views.SkillController.as_view(),name='saveSkills'),
    path('getAllSkillsBySubject/<int:id>/',views.getSkillsBySubject.as_view(),name='getSkills'),
    #Delete data
    path('deletePractice/<int:id>/',views.DeletePractice.as_view(),name='deletePracticeById')
]