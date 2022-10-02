from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ChatMessage, Thread
from accounts.models import GroupProfile


from django.contrib.auth import get_user_model


User = get_user_model()
# Create your views here.

@login_required(login_url='accounts:login')
def chat_home(request):
    user = request.user
    threads = user.thread_set.all()
    template_name = 'chat/chat-home.html'

    return render(request, template_name, {
        'user': user,
        'threads': threads
    })


@login_required(login_url='accounts:login')
def personal_chat(request, username):
    user = request.user
    other_user = User.objects.get(username=username)
    template_name = 'chat/chat.html'
    thread = Thread.objects.get_or_create_personal_thread([user, other_user])
    messages = ChatMessage.objects.filter(thread=thread)
    unread_msgs = messages.filter(read=False)

    for message in unread_msgs:
        if message.sender != user:
            message.read = True
            message.save()
 
    user_threads = user.thread_set.all()
    print(thread.html_id)

    if user == other_user:
        return HttpResponse('Can not caht with yourself')

    if request.method == 'POST':
        chat_message = request.POST['message']
        msg = ChatMessage.objects.create(thread=thread, sender=user, message=chat_message)
        thread.save()

        return render(request, template_name, {
            'user': user,
            'other_user': other_user,
            'thread': thread,
            'messages': messages,
            'user_threads': user_threads,
        })

    return render(request, template_name, {
        'user': user,
        'other_user': other_user,
        'thread': thread,
        'messages': messages,
        'user_threads': user_threads,
    })


@login_required(login_url='accounts:login')
def group_chat_view(request, id):
    user = request.user
    thread = Thread.objects.get(id=id)
    template_name = 'chat/chat.html'
    messages = ChatMessage.objects.filter(thread=thread)
    unread_msgs = messages.filter(read=False)

    for message in unread_msgs:
        if message.sender != user:
            message.read = True
            message.save()


    user_threads = user.thread_set.all()
    print(thread.html_id)

    if user not in thread.users.all():
        thread.users.add(user)

    if request.method == 'POST':
        chat_message = request.POST['message']
        ChatMessage.objects.create(sender=user, thread=thread, message=chat_message)
        thread.save()

        return render(request, template_name, {
            'user': user,
            'thread': thread,
            'messages': messages,
            'user_threads': user_threads
        })

    return render(request, template_name, {
        'user': user,
        'thread': thread,
        'messages': messages,
        'user_threads': user_threads
    })



@login_required(login_url='accounts:login')
def create_new_group_chat(request):
    user = request.user
    group = Thread.objects.create_group_thread()
    group.users.add(user)
    group.save()
    GroupProfile.objects.create(thread=group, owner=user)

    return redirect('chat:group-chat', id=group.id)


@login_required(login_url='accounts:login')
def new_chat(request):
    user = request.user
    template_name = 'chat/new-chat.html'
    context = {'user': user}
    users = User.objects.exclude(username=user.username)
    array = []
    print(users)

    for person in users:
        if not Thread.objects.thread_exists(user, person):
            array.append(person)

    context['array'] = array

    if request.POST:
        th = Thread.objects.create_group_thread()
        GroupProfile.objects.create(creator=user, thread=th, name=request.POST['name'])
        return redirect('chat:group-chat', id=th.id)

    if request.GET.get('query'):
        q = request.GET.get('query')
        print(q)
        users = User.objects.filter(username__icontains=q) | User.objects.filter(first_name__icontains=q ) | User.objects.filter(last_name__icontains=q )
        print(users)
        context['users'] = users

        groups = GroupProfile.objects.filter(name__icontains=q).distinct()
        context['groups'] = groups

    return render(request, template_name, context)


@login_required(login_url='accounts:login')
def go_back(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    if thread.thread_type =='personal':
        if len(thread.chatmessage_set.all()) == 0:
            thread.delete()
    
    return redirect('chat:home')


@api_view(["GET"])
def chats_api(request, username):
    user = User.objects.get(username=username)
    threads = user.thread_set.all().distinct()
    dictionary=[]
    for thread in threads:
        if thread.thread_type == 'personal':
            for person in thread.users.all():
                if person != user:
                    chat = dict(
                        i_d=thread.id,
                        type = 'personal',
                        first_name=person.first_name, 
                        last_name=person.last_name, 
                        image_url=person.userprofile.image.url,
                        username=person.username,
                        chat_id=thread.html_id,
                        last_message = thread.chatmessage_set.all().last().message,
                        sender = thread.chatmessage_set.all().last().sender.username,
                        unread= thread.chatmessage_set.all().last().read
                    )
        else:
            chat = dict(
                i_d=thread.id,
                type='group',
                name = thread.groupprofile.name,
                image_url = thread.groupprofile.image.url,
                id=thread.id,
                chat_id=thread.html_id,                
                last_message= thread.chatmessage_set.all().last().message,
                sender = thread.chatmessage_set.all().last().sender.username,
                unread = thread.chatmessage_set.all().last().read
                
            )

        if chat not in dictionary:
            dictionary.append(chat)

    return Response(dictionary)


def read_message(request, id):
    chat_msg = ChatMessage.objects.get(id=id)
    chat_msg.read = True
    chat_msg.save()

    return JsonResponse({
        'message': chat_msg.message,
        'read': chat_msg.read
    })