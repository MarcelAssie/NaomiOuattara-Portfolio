from django.db.models.deletion import ProtectedError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Category, Project, ProjectMedia
from .forms import CategoryForm, ProjectForm, MultipleProjectMediaForm

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
def dashboard_project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Projet modifié avec succès.")
        return redirect("dashboard")

    return render(request, "dashboard/project_form.html", {
        "form": form,
        "project": project,
        "is_update": True,
    })


# @login_required
def dashboard_project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    try:
        project.delete()
        messages.success(request, "Projet supprimé.")
    except ProtectedError:
        messages.error(request, "Impossible de supprimer ce projet : supprime d’abord les médias associés.")

    return redirect("dashboard")


# @login_required
def dashboard_category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    form = CategoryForm(request.POST or None, instance=category)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Catégorie modifiée.")
        return redirect("dashboard_categories")

    return render(request, "dashboard/categories.html", {
        "form": form,
        "categories": Category.objects.all(),
        "is_update": True,
        "category": category,
    })


# @login_required
def dashboard_category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    try:
        category.delete()
        messages.success(request, "Catégorie supprimée.")
    except ProtectedError:
        messages.error(request, "Impossible de supprimer cette catégorie : des projets y sont encore rattachés.")

    return redirect("dashboard_categories")


# @login_required
def dashboard_project_media(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    form = MultipleProjectMediaForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        print(form.errors)
        print(request.FILES)

    if request.method == "POST" and form.is_valid():
        files = form.cleaned_data["files"]
        media_type = form.cleaned_data["media_type"]
        caption = form.cleaned_data["caption"]

        current_count = project.media.count()

        for index, file in enumerate(files):
            ProjectMedia.objects.create(
                project=project,
                media_type=media_type,
                file=file,
                caption=caption,
                order=current_count + index + 1,
            )

        messages.success(request, "Médias ajoutés avec succès.")
        return redirect("dashboard_project_media", project_id=project.id)

    return render(request, "dashboard/project_media.html", {
        "project": project,
        "form": form,
        "media_list": project.media.all(),
    })


# @login_required
def dashboard_media_delete(request, media_id):
    media = get_object_or_404(ProjectMedia, id=media_id)
    project_id = media.project.id
    media.delete()

    messages.success(request, "Média supprimé.")
    return redirect("dashboard_project_media", project_id=project_id)
