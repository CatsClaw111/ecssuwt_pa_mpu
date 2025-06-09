from django.shortcuts import render
from .models import Project, Category

def index(request):
    projects = Project.objects.order_by('?')[:3]
    return render(request, 'main/index.html', {'projects': projects})

def catalog(request):
    categories = Category.objects.all()
    
    selected_categories = request.GET.getlist('category')
    
    projects = Project.objects.all()
    if selected_categories:
        projects = projects.filter(category__id__in=selected_categories)
    
    return render(request, 'main/catalog.html', {
        'projects': projects,
        'categories': categories,
        'selected_categories': selected_categories,  
    })

    if search_query:
        projects = projects.filter(Q(title__icontains=search_query) | Q(short_description__icontains=search_query))

    if sort == 'newest':
        projects = projects.order_by('-created_at')
    else: 
        projects = projects.order_by('?')

def project(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'main/project.html', {'project': project})

