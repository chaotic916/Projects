from django import forms
from .models import Item

input_class = 'w-full px-6 py-4 rounded_xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category','name','description','price','image','is_sold')
        widgets ={
            'category' : forms.Select(attrs={'class' : input_class}),
            'name': forms.TextInput(attrs={'class': input_class}),
            'description': forms.Textarea(attrs={'class': input_class}),
            'price': forms.TextInput(attrs={'class': input_class}),
            'image': forms.FileInput(attrs={'class': input_class}),
            'is_sold': forms.CheckboxInput(attrs={'class': input_class}),
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name','description','price','image')
        widgets ={
            'name': forms.TextInput(attrs={'class': input_class}),
            'description': forms.Textarea(attrs={'class': input_class}),
            'price': forms.TextInput(attrs={'class': input_class}),
            'image': forms.FileInput(attrs={'class': input_class}),
        }
