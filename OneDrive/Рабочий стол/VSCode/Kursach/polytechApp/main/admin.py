from django.contrib import admin
from . import models

class ProjectImageInline(admin.TabularInline):
    model = models.ProjectImage
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'short_description')
    inlines = [ProjectImageInline]

admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Category)
admin.site.register(models.ProjectImage)
