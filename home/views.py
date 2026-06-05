from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin
from projects_manager.models import Project, Category


CV_FILENAME = "cv.pdf"
CV_DOWNLOAD_NAME = "Ouattara_Naomi_Curriculum Vitae_ Alternance  - CDD-CDI.pdf"
CV_PATH = Path(settings.BASE_DIR) / "static" / "assets" / "docs" / CV_FILENAME


def welcome(request):
    return render(request, 'home/welcome.html')


def about(request):
    featured_projects = Project.objects.filter(is_featured=True)[:3]

    return render(request, "home/about.html", {
        "featured_projects": featured_projects
    })

def contact(request):
    return render(request, "home/contact.html")


def cv(request):
    return render(request, "home/cv.html", {
        "cv_download_name": CV_DOWNLOAD_NAME,
    })


@xframe_options_sameorigin
def cv_view(request):
    return FileResponse(
        CV_PATH.open("rb"),
        as_attachment=False,
        filename=CV_DOWNLOAD_NAME,
        content_type="application/pdf",
    )


def cv_download(request):
    return FileResponse(
        CV_PATH.open("rb"),
        as_attachment=True,
        filename=CV_DOWNLOAD_NAME,
        content_type="application/pdf",
    )


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
    print(related_projects)
    return render(request, "home/details.html", {
        "project": project,
        "media_list": project.media.all(),
        "related_projects": related_projects,
    })
