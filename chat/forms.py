from django import forms

from .models import MessageModel

class MessageForm(forms.Form):
    model = MessageModel
    message = forms.CharField(widget=forms.Textarea)