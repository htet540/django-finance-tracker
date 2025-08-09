from django import forms
from .models import Entity

class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = ['name', 'type', 'location']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }