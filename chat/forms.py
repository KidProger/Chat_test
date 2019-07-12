from django import forms

from django.utils.translation import gettext_lazy as _

from .models import MessageModel, ChatModel

class MessageForm(forms.Form):
    model = MessageModel
    message = forms.CharField(widget=forms.Textarea)


class ChatCreateForm(forms.ModelForm):
    user = forms.CharField(max_length=30, label="User name")
    class Meta:
        model = ChatModel
        fields = ['name']
        labels = {
            'name': _('Chat name'),
        }



