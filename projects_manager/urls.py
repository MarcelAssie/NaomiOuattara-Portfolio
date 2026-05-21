from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/categories/", views.dashboard_categories, name="dashboard_categories"),
    path("dashboard/projects/new/", views.dashboard_project_create, name="dashboard_project_create"),
    path("dashboard/projects/<int:project_id>/media/", views.dashboard_project_media, name="dashboard_project_media"),
]
