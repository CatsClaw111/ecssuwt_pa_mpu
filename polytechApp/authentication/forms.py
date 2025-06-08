from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UsernameField
from .models import Task
from .models import Report  # создадим модель отчёта ниже

class CustomLoginForm(forms.Form):
    username = UsernameField(label='Логин', widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    role = forms.ChoiceField(
        choices=[('student', 'Студент'), ('professor', 'Преподаватель')],
        label="Роль"
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

def clean(self):
    cleaned = super().clean()
    username = cleaned.get("username")
    password = cleaned.get("password")
    role     = cleaned.get("role")
    print("→ clean():", {"username":username, "password":password, "role":role})

    user = authenticate(request=self.request,
                        username=username,
                        password=password)
    print("→ authenticate →", user)
    ...


# authentication/forms.py

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'executor', 'deadline', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Поле executor - только преподаватели из модели Professor
        # Если хочешь, можно ограничить queryset для executor здесь
        # Например:
        # self.fields['executor'].queryset = Professor.objects.all()
        self.fields['deadline'].widget = forms.DateInput(attrs={'type': 'date'})


# authentication/forms.py

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['file']

    file = forms.FileField(label='Загрузить файл отчёта')
