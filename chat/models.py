from django.db import models
from Users.models import CustomUser
from django.urls import reverse

class MessageModel(models.Model):
    date = models.DateTimeField(auto_now=True)
    message = models.TextField(default='')
    user = models.ForeignKey(CustomUser,  on_delete=models.CASCADE)

    def get_absolute_url(self):  # new
        return reverse('chat')
