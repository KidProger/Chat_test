from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from .models import MessageModel, ChatModel
from Users.models import CustomUser
from django.shortcuts import render
from .forms import MessageForm, ChatCreateForm
import datetime


class ChatView(DetailView):
    model = ChatModel
    template_name = 'chat.html'
    form_class = MessageForm
    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = MessageModel()
            message.message = request.POST.get("message")
            message.date = datetime.datetime.now()
            message.author = request.user
            message.chat = ChatModel.objects.get(pk=pk)
            message.save()

            #  chat.user = request.POST.get("user")
            #    chats = ChatModel.objects.create(name=chat.name, user = chat.user)

            #   chat.save()
        #      chat.name = request.POST.get("name")
        #         chat.user = request.POST.get("user")
        #         chat.save()
        #     chat.user.add(user)
        template = self.render_msg(request, pk)
        return template

    def get(self, request, pk):
        template = self.render_msg(request, pk)
        return template

    def render_msg(self, request, pk):
        chats = ChatModel.objects.all()
        user_name_list = []
        user_id_list = []
        for chat in chats:
            for user in chat.user.all():
                user_id_list.append(user.id)
                user_name_list.append(user.username)
            if request.user.id in user_id_list:
                chatForm = ChatCreateForm()
                form = self.form_class()
                if request.user.is_authenticated:
                    username = request.user
                    messages = MessageModel.objects.all()
                    template = render(request, "chat.html",
                                      {"messages": messages, 'form': form, "username": username, "chats": chats,
                                       "chatform": chatForm, "users_id": user_id_list, "users_name": user_name_list,
                                       "primk": pk})
                    return template
        else:
            return HttpResponseRedirect('/chat/createchat')










class ChatCreateView(CreateView):
    model = ChatModel
    form_class = ChatCreateForm
    template_name = "chat_create.html"
    def post(self, request):
        chatForm = ChatCreateForm(request.POST)
        if chatForm.is_valid():
            user = CustomUser.objects.get(username=request.POST.get("user"))
            owner = request.user.username
            chat = ChatModel.objects.create(name=request.POST.get("name"), owner = owner)
            chat.user.add(user)
        return HttpResponseRedirect('/chat/')

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
            message.chat = ChatModel.objects.get(pk=1)
            message.save()


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
        chats = ChatModel.objects.all()
        chatss = ChatModel.objects.filter(user = request.user)
        user_name_list = []
        user_id_list = []
        chat_id = 1
        for chat in chats:
            for user in chat.user.all():
                user_id_list.append(user.id)
                user_name_list.append(user.username)
            if request.user.id in user_id_list:
                chatForm = ChatCreateForm()
                form = self.form_class(initial=self.initial)
                if request.user.is_authenticated:
                    username = request.user
                    messages = MessageModel.objects.all()
                    template = render(request, "send.html", {"messages": messages, 'form': form, "username": username, "chats": chats,
                                                            "chatform": chatForm, "users_id": user_id_list, "users_name": user_name_list,
                                                             "chat_id": chat_id})
                    return template
        else:
            return HttpResponseRedirect('/chat/createchat')