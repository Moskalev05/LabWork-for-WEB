from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, SafetyDocument

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Электронная почта')
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')
    phone = forms.CharField(required=True, label='Телефон')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'company', 'position', 'access_level')
        widgets = {
            'company': forms.TextInput(attrs={'placeholder': 'Не указано'}),
            'position': forms.TextInput(attrs={'placeholder': 'Не указано'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ограничиваем выбор уровня доступа только для админов
        if not kwargs.get('instance') or not kwargs['instance'].is_admin():
            self.fields['access_level'].widget = forms.HiddenInput()

class DocumentForm(forms.ModelForm):
    class Meta:
        model = SafetyDocument
        fields = ['title', 'description', 'category', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название документа'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание документа'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название документа',
            'description': 'Описание',
            'category': 'Категория',
            'file': 'Файл',
        }