from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('cv/', views.cv, name='cv'),
    path('cv/view/', views.cv_view, name='cv_view'),
    path('cv/download/', views.cv_download, name='cv_download'),
    path('projects/', views.projects, name='projects'),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),

]
