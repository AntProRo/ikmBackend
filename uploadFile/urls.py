""" from django.urls import path
from uploadFile.views import uploadFile

urlpatterns = [
    path('u/',uploadFile)
] """

from django.urls import path
from uploadFile import views

urlpatterns = [
    #path('upload/', views.UploadDocument.as_view(), name='upload'),
    path('upload/', views.UploadDocument.as_view(), name='upload'),
    path('getAnalysis/',views.GetAnalysisDocument.as_view(),name='getAnalysis')
    
]