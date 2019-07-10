from django.urls import path

from .views import ChatView, MessageCreateView

urlpatterns = [
    path('', MessageCreateView.as_view(), name='chat'),
    path('', ChatView.as_view(), name='messages')
]