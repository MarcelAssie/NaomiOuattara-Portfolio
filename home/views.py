from django.shortcuts import render
from django.shortcuts import render
from projects_manager.models import Project, Category
def welcome(request):
    return render(request, 'home/welcome.html')


def about(request):
    featured_projects = Project.objects.filter(is_featured=True)[:3]

    return render(request, "home/about.html", {
        "featured_projects": featured_projects
    })


def projects(request):
    created_projects = Project.objects.select_related("category").all()
    categories = Category.objects.all()

    return render(request, "home/projects.html", {
        "projects": created_projects,
        "categories": categories,
    })
