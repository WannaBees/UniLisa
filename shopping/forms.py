from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Model
from django.forms import models


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )



class OrderForm(forms.Form):
    street = forms.CharField(max_length=30, required=True)
    streetnumber= forms.CharField(max_length=30, required=True)
    zip = forms.CharField(max_length=30, required=False)
    city= forms.CharField(max_length=30, required=True)
    country = forms.CharField(max_length=30, required=True)
