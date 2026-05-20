from django.shortcuts import render

def welcome(request):
    return render(request, 'home/welcome.html')

def about(request):
    return render(request, 'home/about.html')

def projects(request):
    return render(request, 'home/projects.html')
