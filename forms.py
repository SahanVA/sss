from pyexpat import model
from attr import fields
from django import forms
from .models import users

class UserForm(forms.ModelForm):
    class Meta:
        model= users
        fields= ["name","username", "password", "photo","status", "level"]