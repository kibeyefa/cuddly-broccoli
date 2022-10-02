from django.urls import path
from .views import chat_home, chats_api, go_back, group_chat_view, new_chat, personal_chat, read_message


app_name = 'chat'

urlpatterns = [
    path('', chat_home, name='home'),
    path('api/<str:username>/', chats_api),
    path('api/messages/<int:id>/', read_message),
    # path('', go_back)
    path('return/<str:thread_id>/', go_back, name='return'),
    path('new/', new_chat, name='new'),
    path('<str:username>/', personal_chat, name='personal-chat'),
    path('groups/<str:id>/', group_chat_view, name='group-chat'),
]