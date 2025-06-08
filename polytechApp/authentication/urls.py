from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home', views.home, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('project/<int:project_id>/work/', views.project_work_view, name='project_work'),
    path('professor/project/<int:project_id>/work/', views.professor_project_work_view, name='professor_project_work'),
    path('task/<int:task_id>/edit/', views.task_edit_view, name='task_edit'),
    path('task/<int:task_id>/create_report/', views.task_create_report_view, name='task_create_report'),

]
