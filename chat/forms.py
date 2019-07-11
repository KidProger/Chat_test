from django import forms

from .models import MessageModel, ChatModel

class MessageForm(forms.Form):
    model = MessageModel
    message = forms.CharField(widget=forms.Textarea)


class ChatCreateForm(forms.ModelForm):
    user = forms.CharField(max_length=30)
    class Meta:
        model = ChatModel
        fields = ['name']
   #     name = forms.CharField(max_length=100)



