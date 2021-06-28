from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import fields
from nocaptcha_recaptcha.fields import NoReCaptchaField
from .models import Customer;



class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    captcha = NoReCaptchaField()
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
    

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField()
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
    class Meta:
        model = User
<<<<<<< HEAD
=======

        fields = ['username','email','first_name','last_name']

>>>>>>> 9e668c9517691bb847ae67f1e88e12d5d24747ec
        fields = ['username','email','first_name','last_name']


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['user','name','email']

