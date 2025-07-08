from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import re


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        error_messages={
            'required': "Email is required",
            'invalid': "Email is invalid"
        }
    )


    username = forms.CharField(
        required=True,
        label="Username",
        error_messages={
            'required': "Username is required",
            'invalid': "Username is invalid"
        }
    )

    password1 = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput,
        error_messages={
            'required': "Password is required",
            'invalid': "Password is invalid"
        }
    )

    password2 = forms.CharField(
        required=True,
        label="Password confirmation",
        widget=forms.PasswordInput,
        error_messages={
            'required': "Repeat password.",
            'invalid': "Passwords don't match"
        }
    )


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username) < 4:
            raise forms.ValidationError("Username must be at least 4 characters long")
        if not re.fullmatch(r"[A-Za-z0-9_.'-]+$", username):
            raise forms.ValidationError("Username must contain only letters, numbers and special characters")

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if len(email) < 6:
            raise forms.ValidationError("Email must be at least 6 characters long")

        return email



class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
