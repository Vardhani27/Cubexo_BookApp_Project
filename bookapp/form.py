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

