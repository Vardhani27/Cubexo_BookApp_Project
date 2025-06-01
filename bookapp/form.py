from django import forms

from .models import User
 
# create a ModelForm
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"