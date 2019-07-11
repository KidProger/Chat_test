from django import forms

from .models import MessageModel, ChatModel

class MessageForm(forms.Form):
    model = MessageModel
    message = forms.CharField(widget=forms.Textarea)


class ChatCreateForm(forms.Form):
    model = ChatModel
    name = forms.CharField(max_length=100)
    user = forms.CharField(max_length=30)