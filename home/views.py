from django.shortcuts import get_object_or_404
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

def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.select_related("category").prefetch_related("media"),
        slug=slug
    )

    related_projects = Project.objects.filter(
        category=project.category
    ).exclude(id=project.id)[:3]

    return render(request, "home/details.html", {
        "project": project,
        "media_list": project.media.all(),
        "related_projects": related_projects,
    })
