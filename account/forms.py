from django import forms
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='Username or Email')
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    photo = forms.ImageField(label='Profile Photo', required=False)
    date_of_birth = forms.DateField(label='Date of Birth', required=False,
                                    widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id) \
            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
