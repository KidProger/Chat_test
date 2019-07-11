from django.urls import path

from .views import  ChatListView, ChatCreateView, ChatView

from django.views.generic import TemplateView

urlpatterns = [
    path('', ChatListView.as_view(),  name='chat'),
    path('createchat/', ChatCreateView.as_view(), name='create'),
    path('<int:pk>/', ChatView.as_view(), name='cheat'),
    path('error', TemplateView.as_view(template_name='errors_chat.html'))
]