from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/categories/", views.dashboard_categories, name="dashboard_categories"),
    path("dashboard/categories/<int:category_id>/edit/", views.dashboard_category_update, name="dashboard_category_update"),
    path("dashboard/categories/<int:category_id>/delete/", views.dashboard_category_delete, name="dashboard_category_delete"),
    path("dashboard/projects/new/", views.dashboard_project_create, name="dashboard_project_create"),
    path("dashboard/projects/<int:project_id>/media/", views.dashboard_project_media, name="dashboard_project_media"),
    path("dashboard/projects/<int:project_id>/edit/", views.dashboard_project_update, name="dashboard_project_update"),
    path("dashboard/projects/<int:project_id>/delete/", views.dashboard_project_delete, name="dashboard_project_delete"),


    path("dashboard/media/<int:media_id>/delete/", views.dashboard_media_delete, name="dashboard_media_delete"),
]
