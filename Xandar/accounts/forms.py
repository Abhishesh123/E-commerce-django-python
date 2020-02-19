from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import Customer


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'gender', 'phone_number',)
