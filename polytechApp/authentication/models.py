# authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from main.models import Project

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('professor', 'Преподаватель'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student', verbose_name="Роль")
    
    def __str__(self):
        return self.username
        

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student', verbose_name='Имя')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='students', verbose_name='Проект')
    group_number = models.CharField(max_length=50, verbose_name="Номер группы")
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

class Professor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='professor')
    department = models.CharField(max_length=100, verbose_name="Кафедра")
    faculty = models.CharField(max_length=100, verbose_name="Факультет")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

class Schedule(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    lesson_no = models.IntegerField()
    day = models.DateField()
    
    def __str__(self):
        return f"Расписание для проекта {self.project.title}"

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"

class Lesson(models.Model):
    time_start = models.TimeField()
    time_end = models.TimeField()
    room_number = models.CharField(max_length=10, verbose_name="Номер аудитории")

    def __str__(self):
        return f"Урок с {self.time_start} до {self.time_end}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    executor = models.ForeignKey(Student, on_delete=models.CASCADE)
    deadline = models.DateField() 
    status = models.CharField(max_length=50, choices=[('pending', 'Ожидает'), ('completed', 'Завершено')], default='pending')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title

class ProfProj(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Преподаватель и проект"
        verbose_name_plural = "Преподаватели и проекты"

    def __str__(self):
        return f"{self.professor.user.username} - {self.project.title}"

class Report(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reports')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='reports/')

    def __str__(self):
        return f"Отчёт по задаче ({self.task.title})"

