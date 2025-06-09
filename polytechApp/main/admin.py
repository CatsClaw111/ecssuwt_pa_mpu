from django.contrib import admin
from .models import Project, Category, ProjectImage

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'short_description')
    date_hierarchy = 'created_at'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project',)
    list_filter = ('project',)