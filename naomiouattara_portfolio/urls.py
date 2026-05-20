"""
URL configuration for cmcimediaplatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls"))
]


if settings.DEBUG:
    urlpatterns += [
        # URLs pour tester les pages d'erreur en développement
        path("test-404/", views.custom_404),
        path("test-500/", views.custom_500),
        path("test-403/", views.custom_403),
        path("test-400/", views.custom_400),
    ]

    if not getattr(settings, "USE_AWS", False):
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

handler404 = "naomiouattara_portfolio.views.custom_404"
handler500 = "naomiouattara_portfolio.views.custom_500"
handler403 = "naomiouattara_portfolio.views.custom_403"
handler400 = "naomiouattara_portfolio.views.custom_400"
