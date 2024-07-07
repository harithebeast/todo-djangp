# forms.py

from django import forms
from .models import todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = todo
        fields = ['todo_name', 'status']  # List the fields you want to include in the edit form
        widgets = {
            'todo_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a task here'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
