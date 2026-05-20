from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render


def custom_404(request, exception=None):
    """Vue personnalisée pour les erreurs 404"""
    context = {
        "error_code": 404,
        "error_message": "Page non trouvée",
        "error_description": "La page que vous recherchez n'existe pas ou a été déplacée.",
    }
    return HttpResponseNotFound(render(request, "errors/404.html", context))


def custom_500(request):
    """Vue personnalisée pour les erreurs 500"""
    context = {
        "error_code": 500,
        "error_message": "Erreur serveur",
        "error_description": "Une erreur interne du serveur s'est produite.",
    }
    return HttpResponseServerError(render(request, "errors/500.html", context))


def custom_403(request, exception=None):
    """Vue personnalisée pour les erreurs 403"""
    context = {
        "error_code": 403,
        "error_message": "Accès refusé",
        "error_description": "Vous n'avez pas l'autorisation d'accéder à cette page.",
    }
    return HttpResponseForbidden(render(request, "errors/403.html", context))


def custom_400(request, exception=None):
    """Vue personnalisée pour les erreurs 400"""
    context = {
        "error_code": 400,
        "error_message": "Requête incorrecte",
        "error_description": "La requête envoyée au serveur est incorrecte.",
    }
    return HttpResponseBadRequest(render(request, "errors/400.html", context))
