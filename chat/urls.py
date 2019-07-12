from django.urls import path

from .views import  ChatListView, ChatCreateView, ChatView, UserAddView

from django.views.generic import TemplateView

urlpatterns = [
    path('', ChatListView.as_view(),  name='chat_list'),
    path('createchat/', ChatCreateView.as_view(), name='create'),
    path('adduser/', UserAddView.as_view(), name='add'),
    path('<int:pk>/', ChatView.as_view(), name='chat'),
    path('error/', TemplateView.as_view(template_name='errors_chat.html')),
    path('not_auth/', TemplateView.as_view(template_name='auth.html')),
    path('test/', TemplateView.as_view(template_name='test.html')),
]