from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Task
from .models import Report  # создадим модель отчёта ниже


class CustomLoginForm(AuthenticationForm):
    username = UsernameField(
        label='Логин',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput
    )


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



User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'executor', 'deadline', 'status']
        widgets = {
            # указываем формат ISO, чтобы value="YYYY-MM-DD" подхватывался браузером
            'deadline': forms.DateInput(format='%Y-%m-%d', attrs={
                'type': 'date',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # если передан instance (режим редактирования), вручную положим initial
        if self.instance and self.instance.pk:
            self.fields['deadline'].initial = self.instance.deadline.strftime('%Y-%m-%d')

# authentication/forms.py

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['file']

    file = forms.FileField(label='Загрузить файл отчёта')
