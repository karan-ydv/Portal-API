from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view()),
    path('register/', views.RegistrationView),
    path('adminapi/', views.AdminLoginView),
    path('login/', views.StudentLoginView)
]