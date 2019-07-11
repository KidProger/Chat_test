from django.urls import path

from .views import  MessageCreateView, ChatCreateView, ChatView

urlpatterns = [
    path('', MessageCreateView.as_view(),  name='chat'),
    path('createchat/', ChatCreateView.as_view(), name='create'),
    path('<int:pk>/', ChatView.as_view(), name='cheat'),
]