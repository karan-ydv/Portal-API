from django.urls import path, include
from . import views

urlpatterns = [
    path('questions/', views.QuestionsView),
    path('test/', views.TestView),
    path('response/', views.ResponseView)
]