from django import forms
from .models import Message

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class':'w-full px-6 py-4 rounded-xl border'
            })
        }