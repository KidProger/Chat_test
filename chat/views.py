from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from .models import MessageModel
from django.shortcuts import render
from .forms import MessageForm
import datetime


class ChatView(ListView):
    model = MessageModel
    template_name = "chat.html"
    context_object_name = 'all_chat_list'


class MessageCreateView(CreateView):
    model = MessageModel
    template_name = "send.html"
    form_class = MessageForm
    fields = '__all__'
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = MessageModel()
            message.message =  request.POST.get("message")
            message.date = datetime.datetime.now()
            message.user = request.user
            message.save()
        return self.get(request)

    def get(self, request):
        form = self.form_class(initial=self.initial)
        messages = MessageModel.objects.all()
        if request.user.is_authenticated:
            username = request.user.username
        return render(request, "send.html", {"messages": messages, 'form': form, "username": username})
