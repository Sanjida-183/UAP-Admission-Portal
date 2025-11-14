# forms.py - COMPLETE FILE
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Student, Department

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    student_id = forms.CharField(max_length=20, required=True)
    phone = forms.CharField(max_length=15, required=False)
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(), 
        required=False
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            student = Student.objects.create(
                user=user,
                student_id=self.cleaned_data['student_id'],
                phone=self.cleaned_data['phone'],
                department=self.cleaned_data['department']
            )
        return user

class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username or Student ID'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    