from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),

]
