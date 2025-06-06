from django.contrib import admin
from .models import CustomUser, Student, Professor, Task, Schedule, Lesson, ProfProj

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)
    search_fields = ('username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Task)
admin.site.register(Schedule)
admin.site.register(Lesson)
admin.site.register(ProfProj)
