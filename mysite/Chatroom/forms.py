from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class RegistrationForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    email = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email = email)
            print(User.objects.get(email = email))
        except ObjectDoesNotExist:
            return email
        else:
            raise forms.ValidationError('E-mail taken')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            return username
        else:
            raise forms.ValidationError('Username taken')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            raise forms.ValidationError('Username does not exists')
        else:
            return username
