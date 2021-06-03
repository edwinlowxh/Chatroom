from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length = 20)
    password1 = forms.CharField(max_length = 20)
    password2 = forms.CharField(max_length = 20)
    email = forms.CharField(max_length = 50)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
