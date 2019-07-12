from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from .models import MessageModel, ChatModel
from Users.models import CustomUser
from django.shortcuts import render
from .forms import MessageForm, ChatCreateForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
import datetime


class ChatView(DetailView):
    model = ChatModel
    template_name = 'chat.html'
    form_class = MessageForm

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """ Takes input messages from chat, check for valid and save it to database.  """
        form = self.form_class(request.POST)
        if form.is_valid():
            message = MessageModel()
            message.message = request.POST.get("message")
            message.date = datetime.datetime.now()
            message.author = request.user
            message.chat = ChatModel.objects.get(pk=pk)
            message.save()
        template = self.render_page(request, pk)
        return template




    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """ Accepts Get request and render template with a call to the render_page  """
        template = self.render_page(request, pk)
        return template


    def render_page(self, request: HttpRequest, pk: int) -> HttpResponse:
        """ Check for authorization. Select data from database and render it in chat.html"""
        user_name_list = []
        current_chat = ChatModel.objects.get(pk=pk)
        user_name_list.append(current_chat.owner)
        for user in current_chat.user.filter():
            user_name_list.append(user.username)

        if request.user.is_authenticated and request.user.username in user_name_list:
            user_all_chats_list = []
            user_chat_list = ChatModel.objects.filter(user=request.user)
            for chat in user_chat_list:
                user_all_chats_list.append(chat.id)
            owner_chat_list = ChatModel.objects.filter(owner=request.user)
            for chat in owner_chat_list:
                user_all_chats_list.append(chat.id)
            all_chats = ChatModel.objects.all()
            user_id_list = []
            for chat in all_chats:
                for user in chat.user.all():
                    user_id_list.append(user.id)
            messages =  MessageModel.objects.filter(chat = ChatModel.objects.get(pk=pk))
            template = render(request, "chat.html", {"messages": messages, 'form': self.form_class(), "username": request.user,
                                                     "chats": all_chats, "users_id": user_id_list, "users_name": set(user_name_list),
                                                     "pk": pk, "chat_list": set(user_all_chats_list)})
            return template
        else:
            return HttpResponseRedirect('/chat/error')


class ChatCreateView(CreateView):
    model = ChatModel
    form_class = ChatCreateForm
    template_name = "chat_create.html"
    def post(self, request: HttpRequest) -> HttpResponse:
        """ Check for valid data, create new chat and redirect"""
        chatForm = ChatCreateForm(request.POST)
        if chatForm.is_valid():
            try:
                message = "Error: User doesn't exist"
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
        else:
            return render(request, "errors_chat.html", {"message": "Chat is exist"})

    def get(self, request: HttpRequest) -> HttpResponse:
        chatForm = ChatCreateForm()
        chats = ChatModel.objects.all()
        chat_list = []
        for chat in chats:
            chat_list.append(chat.name)
        users = CustomUser.objects.all()
        user_list = []
        for user in users:
            user_list.append(user.username)
        return render(request, self.template_name, {"users": user_list, "chatform": chatForm, "chat_list": chat_list})

class UserAddView(CreateView):
    model = ChatModel
    form_class = ChatCreateForm
    template_name = "user_add.html"
    def post(self, request: HttpRequest) -> HttpResponse:
        """ Check for valid data, add new user for chat and redirect"""
        chatForm = ChatCreateForm(request.POST)
        if chatForm.is_valid():
            try:
                message = "Error: User doesn't exist"
                user = CustomUser.objects.get(username=request.POST.get("user"))

            except ObjectDoesNotExist:
                return render(request, "errors_chat.html", {"message": message})
            owner = request.user.username
            if user.username == owner:
                message = "Error: You can't add yourself to chat"
                return render(request, "errors_chat.html", {"message": message})
            try:
                message = "Error: Chat doesn't exist"
                chat = ChatModel.objects.get(name=request.POST.get("name"))
            except ObjectDoesNotExist:
                return render(request, "errors_chat.html", {"message": message})
            chat.user.add(user)
            return HttpResponseRedirect('/chat/')
        else:
            return HttpResponseRedirect('/chat/error')

    def get(self, request: HttpRequest) -> HttpResponse:
        chatForm = ChatCreateForm()
        chats = ChatModel.objects.all()
        chat_list = []
        for chat in chats:
            chat_list.append(chat.name)
        users = CustomUser.objects.all()
        user_list = []
        for user in users:
            user_list.append(user.username)
        return render(request, self.template_name, {"user_list": user_list, "chatform": chatForm, "chat_list": chat_list})


class ChatListView(ListView):
    model = ChatModel
    template_name = "chat_list.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """ Check for authorization. Select all available chats for user and render it"""
        if request.user.is_authenticated:
            chats_list = []
            user_chat_list = ChatModel.objects.filter(user = request.user)
            for chat in user_chat_list:
                chats_list.append(chat.id)
            owner_chat_list = ChatModel.objects.filter(owner = request.user)
            for chat in owner_chat_list:
                    chats_list.append(chat.id)
            return render(request, "chat_list.html", {"chats": set(chats_list)})
        else:
            return HttpResponseRedirect('/chat/not_auth/')