from django.shortcuts import render
from .models import Project, Category

def index(request):
    projects = Project.objects.order_by('?')[:3]  # Выбираем 3 случайных проекта
    return render(request, 'main/index.html', {'projects': projects})

def catalog(request):
    projects = Project.objects.all()
    categories = Category.objects.all()
    return render(request, 'main/catalog.html', {'projects': projects, 'categories': categories})

def project(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'main/project.html', {'project': project})