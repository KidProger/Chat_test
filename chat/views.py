from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from .models import MessageModel, ChatModel
from Users.models import CustomUser
from django.shortcuts import render
from .forms import MessageForm, ChatCreateForm
import datetime



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
        chatForm = ChatCreateForm(request.POST)
        if chatForm.is_valid():
            user = CustomUser.objects.get(username=request.POST.get("user"))
            chat = ChatModel.objects.create(name=request.POST.get("name"))
            chat.user.add(user)

            #  chat.user = request.POST.get("user")
                 #    chats = ChatModel.objects.create(name=chat.name, user = chat.user)

                  #   chat.save()
          #      chat.name = request.POST.get("name")
       #         chat.user = request.POST.get("user")
       #         chat.save()
           #     chat.user.add(user)
        template = self.render_msg(request)
        return template

    def get(self, request):
         template = self.render_msg(request)
         return template


    def render_msg(self, request):
        chats = ChatModel.objects.filter(user=request.user)
        chatForm = ChatCreateForm()
        form = self.form_class(initial=self.initial)
        if request.user.is_authenticated:
            username = request.user
        messages = MessageModel.objects.all()
        template = render(request, "send.html", {"messages": messages, 'form': form, "username": username, "chats": chats,
                                                "chatform": chatForm})
        return template