from django import forms
from .models import Livestock

class LivestockForm(forms.ModelForm):
    class Meta:
        model = Livestock
        fields = ['name', 'category', 'weight', 'age', 'price', 'description', 'image']
