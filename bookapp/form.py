<<<<<<< HEAD
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'pages', 'category', 'cover', 'pdf_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
        }

=======
from django import forms

from .models import User
 
# create a ModelForm
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
>>>>>>> 91cc36d3eb3bd182817efc3ff53ca5e604607ad6
