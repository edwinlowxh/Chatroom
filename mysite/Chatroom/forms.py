from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length = 50)
    first_name = forms.CharField(max_length = 50)
    last_name = forms.CharField(max_length = 50)
    password1 = forms.CharField()
    password2 = forms.CharField()
    email = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')

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

        if (len(username) > 50):
            raise forms.ValidationError('Username must be less than 50 characters')
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            return username
        else:
            raise forms.ValidationError('Username taken')

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if (len(first_name) > 50):
            raise forms.ValidationError('First name must be less than 50 characters')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if (len(last_name) > 50):
            raise forms.ValidationError('Last name must be less than 50 characters')

        return last_name


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
            raise forms.ValidationError('Username does not exist')
        else:
            return username