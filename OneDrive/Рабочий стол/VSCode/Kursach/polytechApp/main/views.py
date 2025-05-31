from django.shortcuts import render
from .models import Project, Category
from django.db.models import Q

def index(request):
    projects = Project.objects.order_by('?')[:3]
    return render(request, 'main/index.html', {'projects': projects})

def catalog(request):
    categories = Category.objects.all()
    
    selected_categories = request.GET.getlist('category')
    
    search_query = request.GET.get('q', '')
    
    sort = request.GET.get('sort', 'popularity')
    
    projects = Project.objects.all()
    
    if selected_categories:
        projects = projects.filter(category__id__in=selected_categories)
    
    if search_query:
        projects = projects.filter(Q(title__icontains=search_query) | Q(short_description__icontains=search_query))
    
    # Сортировка
    if sort == 'newest':
        projects = projects.order_by('-created_at')
        projects = projects.order_by('?')
    
    return render(request, 'main/catalog.html', {
        'projects': projects,
        'categories': categories,
        'selected_categories': selected_categories,
        'search_query': search_query,
        'sort': sort,
    })

def project(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'main/project.html', {'project': project})