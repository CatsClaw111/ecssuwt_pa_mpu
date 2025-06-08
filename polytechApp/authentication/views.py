from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from main.models import Project
from .models import Student, Professor, Task, ProfProj
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import CustomLoginForm, ReportForm, TaskForm
from django.db import connection
from time import timezone
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

def login_view(request):
    next_url = request.GET.get('next', 'dashboard')
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(next_url)
        messages.error(request, "Неверный логин или пароль.")
    else:
        form = CustomLoginForm(request)
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'main/index.html')

@login_required
def student_profile(request):
    student = request.user.student
    return render(request, 'authentication/student_profile.html', {'student': student})

@login_required
def professor_profile(request):
    professor = request.user.professor
    projects = professor.projects.all()
    return render(request, 'authentication/professor_profile.html', {'professor': professor, 'projects': projects})

@login_required
def dashboard_view(request):
    user = request.user

    if user.role == 'professor':
        professor = user.professor  # Получаем объект преподавателя

        # Получаем проекты преподавателя через промежуточную модель ProfProj
        projects = ProfProj.objects.filter(professor=professor).select_related('project')

        context = {
            'professor': professor,
            'projects': [prof_proj.project for prof_proj in projects],  # Список проектов
        }
        return render(request, 'authentication/professor_dashboard.html', context)

    elif user.role == 'student':
        # Логика для студента
        student = user.student  # Получаем объект студента
        project = student.project  # Получаем проект, к которому прикреплён студент

        context = {
            'student': student,
            'project': project,  # Проект, к которому прикреплён студент
        }
        return render(request, 'authentication/student_dashboard.html', context)

    else:
        # Если роль не соответствует преподавателю или студенту, например, администратор
        return render(request, 'authentication/login.html', {'user': user})

@login_required
def project_work_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Доступ студента
    user = request.user
    if user.role != 'student' or not hasattr(user, 'student') or user.student.project != project:
        return render(request, 'authentication/no_access.html')

    # Настройки сортировки
    allowed = {
        'title':       'title',
        'description': 'description',
        'executor':    'executor__user__username',
        'deadline':    'deadline',
        'status':      'status',
    }
    sort = request.GET.get('sort', 'deadline')
    desc = sort.startswith('-')
    key = sort.lstrip('-')
    field = allowed.get(key, allowed['deadline'])
    order = ('-' if desc else '') + field

    # Выбираем задачи и сортируем
    tasks = project.tasks.select_related('executor__user').order_by(order)

    # Передаём колоноки, выборку и текущий сорт
    columns = [
        ('title',       'Название задачи'),
        ('description', 'Описание'),
        ('executor',    'Исполнитель'),
        ('deadline',    'Дедлайн'),
        ('status',      'Статус'),
    ]

    return render(request, 'authentication/project_work.html', {
        'project':      project,
        'tasks':        tasks,
        'columns':      columns,
        'current_sort': sort,
    })

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('professor_project_work', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'authentication/task_form.html', {
        'form': form,
        'project': project,
    })


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('professor_project_work', project_id=project.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'authentication/task_form.html', {
        'form': form,
        'project': project,
        'task': task,
    })

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    if request.method == 'POST':
        task.delete()
        return redirect('professor_project_work', project_id=project.id)
    return render(request, 'authentication/task_confirm_delete.html', {
        'task': task,
    })


@login_required
def task_create_report_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    user = request.user

    # Проверка доступа: студент должен быть ответственным или преподаватель прикреплен к проекту
    if user.role == 'student':
        if not hasattr(user, 'student') or user.student != task.executor:
            return redirect('dashboard')
    elif user.role == 'professor':
        if task.project not in user.professor.projects.all():
            return redirect('dashboard')
    else:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.task = task
            report.save()
            return redirect('project_work', project_id=task.project.id)
    else:
        form = ReportForm()

    return render(request, 'authentication/task_create_report.html', {'form': form, 'task': task})

@login_required
def professor_project_work_view(request, project_id):
    professor = request.user.professor
    project = get_object_or_404(Project, id=project_id)

    if not ProfProj.objects.filter(professor=professor, project=project).exists():
        return render(request, 'authentication/error.html', {
            'message': 'Проект не найден для данного преподавателя'
        })

    # Настройки для сортировки
    allowed = {
        'title':       'title',
        'description': 'description',
        'executor':    'executor__user__username',
        'deadline':    'deadline',
        'status':      'status',
    }
    sort = request.GET.get('sort', 'deadline')
    desc = sort.startswith('-')
    key = sort.lstrip('-')
    field = allowed.get(key, allowed['deadline'])
    order = ('-' if desc else '') + field

    tasks = project.tasks.select_related('executor__user').order_by(order)

    columns = [
        ('title',       'Название задачи'),
        ('description', 'Описание'),
        ('executor',    'Исполнитель'),
        ('deadline',    'Дедлайн'),
        ('status',      'Статус'),
    ]

    context = {
        'professor':    professor,
        'project':      project,
        'tasks':        tasks,
        'current_sort': sort,
        'columns': columns,
    }
    return render(request, 'authentication/professor_work.html', context)



def execute_query():
    with connection.cursor() as cursor:
        # Создание индекса для ускорения поиска по проектам в таблице задач
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_project_id ON tasks (project_id);
        """)

        # Уникальный индекс для пар "проект - исполнитель"
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_project_executor ON tasks (project_id, executor_id);
        """)

        # Функция для обновления метки времени при изменении задачи
        cursor.execute("""
            CREATE OR REPLACE FUNCTION update_task_timestamp() 
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at := CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)

        # Триггер для обновления времени при изменении задачи
        cursor.execute("""
            DROP TRIGGER IF EXISTS trigger_update_task_timestamp ON tasks;
            CREATE TRIGGER trigger_update_task_timestamp
            BEFORE UPDATE ON tasks
            FOR EACH ROW
            EXECUTE FUNCTION update_task_timestamp();
        """)

        # Функция для предотвращения удаления проекта, если к нему прикреплены задачи
        cursor.execute("""
            CREATE OR REPLACE FUNCTION prevent_project_deletion() 
            RETURNS TRIGGER AS $$
            BEGIN
                IF EXISTS (SELECT 1 FROM tasks WHERE project_id = OLD.id) THEN
                    RAISE EXCEPTION 'Невозможно удалить проект, к нему прикреплены задачи';
                END IF;
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
        """)

        # Триггер для предотвращения удаления проекта
        cursor.execute("""
            DROP TRIGGER IF EXISTS trigger_prevent_project_deletion ON projects;
            CREATE TRIGGER trigger_prevent_project_deletion
            BEFORE DELETE ON projects
            FOR EACH ROW
            EXECUTE FUNCTION prevent_project_deletion();
        """)

        # Создание представления для всех задач с проектами и исполнителями
        cursor.execute("""
            CREATE VIEW IF NOT EXISTS task_overview AS
            SELECT 
                t.id AS task_id,
                t.title AS task_title,
                p.title AS project_title,
                u.username AS executor_name,
                t.deadline,
                t.status
            FROM 
                tasks t
            JOIN 
                projects p ON t.project_id = p.id
            JOIN 
                users u ON t.executor_id = u.id;
        """)



def update_task_status(request, task_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')  # Получаем новый статус из формы или запроса
        
        # Получаем задачу по ID
        task = get_object_or_404(Task, id=task_id)
        
        try:
            # Обновляем статус задачи
            task.status = new_status
            task.completion_date = timezone.now()
            task.save()
            
            # Отправляем уведомление
            send_task_notification(task.id, new_status)
            
            return JsonResponse({'success': True, 'message': f'Задача {task_id} обновлена на статус {new_status}'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"Ошибка при обновлении статуса задачи: {e}"})
        
    return JsonResponse({'success': False, 'message': 'Неверный метод запроса'})

def send_task_notification(task_id, new_status):
    # Логика для отправки уведомлений студентам и преподавателям
    print(f"Задача {task_id} была обновлена на статус: {new_status}")






# from django.shortcuts import HttpResponse

# def debug_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             return HttpResponse("УСПЕХ")
#         else:
#             print("AuthForm errors:", form.errors)
#     else:
#         form = AuthenticationForm(request)
#     return render(request, 'authentication/login.html', {'form': form})
