from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from .models import MessageModel, ChatModel
from Users.models import CustomUser
from django.shortcuts import render
from .forms import MessageForm, ChatCreateForm
from django.core.exceptions import ObjectDoesNotExist
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
        template = self.render_msg(request, pk)
        return template

    def get(self, request, pk):
        template = self.render_msg(request, pk)
        return template

    def render_msg(self, request, pk):
        chats_list = []
        user_chat_list = ChatModel.objects.filter(user=request.user)
        for chat in user_chat_list:
            chats_list.append(chat.id)
        owner_chat_list = ChatModel.objects.filter(owner=request.user)
        for chat in owner_chat_list:
            chats_list.append(chat.id)
        chats = ChatModel.objects.all()
        user_name_list = []
        user_id_list = []
        current_chat = ChatModel.objects.get(pk=pk)
        user_name_list.append(current_chat.user.get().username)
        user_name_list.append(current_chat.owner)
        if request.user.is_authenticated and request.user.username in user_name_list:
            for chat in chats:
                for user in chat.user.all():
                    user_id_list.append(user.id)

                if request.user.id in user_id_list:
                     chatForm = ChatCreateForm()
                     form = self.form_class()
                     username = request.user
                 #    messages = MessageModel.objects.all()
                     messages =  MessageModel.objects.filter(chat = ChatModel.objects.get(pk=pk))
                     template = render(request, "chat.html",
                                          {"messages": messages, 'form': form, "username": username, "chats": chats,
                                          "chatform": chatForm, "users_id": user_id_list, "users_name": user_name_list,
                                          "primk": pk, "chat_list": set(chats_list)})
                     return template
        else:
             return HttpResponseRedirect('/chat/error')


class ChatCreateView(CreateView):
    model = ChatModel
    form_class = ChatCreateForm
    template_name = "chat_create.html"
    def post(self, request):
        chatForm = ChatCreateForm(request.POST)
        if chatForm.is_valid():
            try:
                message = "Error: unregistered user"
                user = CustomUser.objects.get(username=request.POST.get("user"))
            except ObjectDoesNotExist:
                return render(request, "errors_chat.html", {"message": message})
            owner = request.user.username
            if user.username == owner:
                message = "Error: You can't create chat with yourself"
                return render(request, "errors_chat.html", {"message": message})
            chat = ChatModel.objects.create(name=request.POST.get("name"), owner = owner)
            chat.user.add(user)
            return HttpResponseRedirect('/chat/')


class ChatListView(ListView):
    model = ChatModel
    template_name = "send.html"

    def get(self, request):
        chats_list = []
        user_chat_list = ChatModel.objects.filter(user = request.user)
        for chat in user_chat_list:
            chats_list.append(chat.id)
        owner_chat_list = ChatModel.objects.filter(owner = request.user)
        for chat in owner_chat_list:
                chats_list.append(chat.id)
        return render(request, "send.html", {"chats": set(chats_list)})
