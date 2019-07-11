from django.db import models
from Users.models import CustomUser
from django.urls import reverse


class ChatModel(models.Model):
    user = models.ManyToManyField(CustomUser)
    name = models.CharField(max_length=100, default="")
    def get_absolute_url(self):  # new
        return reverse('chat')

class MessageModel(models.Model):
    date = models.DateTimeField(auto_now=True)
    message = models.TextField(default='')
    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)
    chat = models.ForeignKey(ChatModel,  on_delete=models.CASCADE, default="")

    def get_absolute_url(self):  # new
        return reverse('chat')




