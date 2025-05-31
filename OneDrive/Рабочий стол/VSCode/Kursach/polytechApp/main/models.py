from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class ProjectImage(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='images', verbose_name="Проект")
    image = models.ImageField(upload_to='projects/images/', verbose_name="Изображение")
    
    def __str__(self):
        return f"Изображение для {self.project.title}"
    
    class Meta:
        verbose_name = "Изображение проекта"
        verbose_name_plural = "Изображения проектов"

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    main_image = models.ImageField(upload_to='projects/images/', verbose_name="Основное изображение")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    duration = models.IntegerField(verbose_name="Срок выполнения (дней)")
    short_description = models.TextField(verbose_name="Краткое описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"