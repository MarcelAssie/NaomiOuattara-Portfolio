from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Project, ProjectMedia
from .forms import CategoryForm, ProjectForm, ProjectMediaForm


# @login_required
def dashboard(request):
    projects = Project.objects.all()
    categories = Category.objects.all()

    return render(request, "dashboard/admin.html", {
        "projects": projects,
        "categories": categories,
    })


# @login_required
def dashboard_categories(request):
    form = CategoryForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard_categories")

    categories = Category.objects.all()

    return render(request, "dashboard/categories.html", {
        "form": form,
        "categories": categories,
    })


# @login_required
def dashboard_project_create(request):
    form = ProjectForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        project = form.save()
        return redirect("dashboard_project_media", project_id=project.id)

    return render(request, "dashboard/project_form.html", {
        "form": form,
    })


# @login_required
def dashboard_project_media(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    form = ProjectMediaForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        media = form.save(commit=False)
        media.project = project
        media.save()
        return redirect("dashboard_project_media", project_id=project.id)

    media_list = project.media.all()

    return render(request, "dashboard/project_media.html", {
        "project": project,
        "form": form,
        "media_list": media_list,
    })
