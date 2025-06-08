from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Student, Professor, Task, Schedule, Lesson, ProfProj, Report

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # какие колонки выводим в списке
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser', 'is_active')
    list_filter  = ('role', 'is_staff', 'is_superuser', 'is_active')

    # в какие секции разбита форма редактирования
    fieldsets = (
        (None,               {'fields': ('username', 'password')}),
        ('Личные данные',    {'fields': ('first_name', 'last_name', 'email')}),
        ('Разрешения',       {'fields': ('role', 'is_active', 'is_staff', 'is_superuser',
                                         'groups', 'user_permissions')}),
        ('Важные даты',      {'fields': ('last_login', 'date_joined')}),
    )

    # секция «Add user» — та самая, где спрашивает password1/password2
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'email')
    ordering     = ('username',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'group_number', 'project')
    list_filter = ('group_number', 'project')
    search_fields = ('user__username', 'group_number', 'project__title')

    raw_id_fields = [
        'user',
    ]

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'faculty')
    list_filter = ('department', 'faculty')
    search_fields = ('user__username', 'department', 'faculty')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'executor', 'status', 'deadline', 'project')
    list_filter = ('status', 'project', 'deadline')
    search_fields = ('title', 'executor__user__username', 'project__title')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('project', 'lesson', 'lesson_no', 'day')
    list_filter = ('day', 'project')
    search_fields = ('project__title', 'lesson__room_number')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('time_start', 'time_end', 'room_number')
    search_fields = ('room_number',)


@admin.register(ProfProj)
class ProfProjAdmin(admin.ModelAdmin):
    list_display = ('professor', 'project')
    search_fields = ('professor__user__username', 'project__title')
    list_filter = ('project',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('task', 'uploaded_at')
    search_fields = ('task__title',)
    list_filter = ('uploaded_at',)
