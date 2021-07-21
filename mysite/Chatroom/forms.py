from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import groups


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

class NewGroupForm(forms.Form):
    OPTIONS = ((user.id, user.username) for user in User.objects.all().exclude(is_superuser = True))
    group_name = forms.CharField(max_length = 50)
    users_to_add = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices = OPTIONS)

    def clean_group_name(self):
        group_name = self.cleaned_data['group_name']
        if (len(group_name) > 50):
            raise forms.ValidationError('Group name must be less than 50 characters')
        try:
            groups.objects.get(group_name = group_name)
        except ObjectDoesNotExist:
            return group_name
        else:
            raise forms.ValidationError('Group name taken')

class changePasswordForm(forms.Form):
    password = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()


    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user.check_password(password):
            raise forms.ValidationError('Invalid old password')
        else:
            return password

    def clean_password1(self):

        password1 = self.cleaned_data['password1']

        try:
            validate_password(password1, self.user)
        except ValidationError as e:
            raise ValidationError(e)

        return password1

    def clean_password2(self):
        password2 = self.cleaned_data['password2']

        try:
            password = self.cleaned_data['password1']
        except KeyError:
            # If password1 has a ValidationError
            return

        if (password != password2):
            raise forms.ValidationError('Passwords do not match')

        return password2

    def __init__(self, *args,**kwargs):
        self.user = kwargs.pop('user')
        super(changePasswordForm, self).__init__(*args,**kwargs)
