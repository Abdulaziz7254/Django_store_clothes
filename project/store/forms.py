from django import forms
from django.contrib.auth.models import User  # Стандартная модель пользователя
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Address


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']








class AddressForm(forms.ModelForm):
     class Meta:
         model = Address
         fields = ['city', 'street', 'house', 'zipcode']
         widgets = {
             'city': forms.TextInput(attrs={
                 'class': 'form-control'
             }),
             'street': forms.TextInput(attrs={
                 'class': 'form-control'
             }),
             'house': forms.TextInput(attrs={
                'class': 'form-control'
             }),
            'zipcode': forms.TextInput(attrs={
                 'class': 'form-control'
             })
         }