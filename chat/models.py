from django.db import models

from Users.models import CustomUser

from django.urls import reverse


class ChatModel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    user = models.ManyToManyField(CustomUser)
    def get_absolute_url(self):  # new
        return reverse('chat')

class MessageModel(models.Model):
    date = models.DateTimeField(auto_now=True)
    message = models.TextField()
    author = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)
    chat = models.ForeignKey(ChatModel,  on_delete=models.CASCADE)
    def get_absolute_url(self):  # new
        return reverse('chat')




