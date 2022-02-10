from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','password')

    def clean(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Email or Password")
