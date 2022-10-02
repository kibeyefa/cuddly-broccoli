import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread, ChatMessage


User = get_user_model()

class GroupChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.user = self.scope['user']
        self.thread_id = self.scope['url_route']['kwargs']['id']
        self.thread = await self.get_thread()
        self.group_name = str(self.thread_id)
        all_threads = await self.get_all_threads()
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print(all_threads)
        for thread in all_threads:
            await self.channel_layer.group_add(thread, self.channel_name)

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_disconnect(self, event):
        pass

    async def websocket_receive(self, event):
        message = json.loads(event['text'])
        msg = message['message']
        print(f'message: {msg}')
        chat_message = await self.create_messsage(self.user, self.thread, msg)
        print(chat_message.message)
        print(event)
        await self.channel_layer.group_send(self.group_name, {
            'type': 'websocket.message',
            'text': event['text']
        })

    async def websocket_message(self, event):
        print(event)
        event_details = json.loads(event['text']) 
        chat_message = event_details['message']
        sender = event_details['sender']
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps({
                'chat_message': chat_message,
                'sender': sender,
                'title': event_details['title'],
                'image_url': event_details['image_url'],
                'html_id': event_details['hmtl_id']
            })
        })

    @database_sync_to_async
    def get_thread(self):
        return Thread.objects.get(id=self.thread_id)

    @database_sync_to_async
    def create_messsage(self, sender, thread, message):
        chat_message = ChatMessage.objects.create(sender=sender, thread=thread, message=message)
        thread.save()
        return chat_message

    @database_sync_to_async
    def get_all_threads(self):
        all_threads = [str(thread.id) for thread in self.user.thread_set.all() if thread.id != self.thread.id]
        print(all_threads)
        return all_threads



class PrivateChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.user = self.scope['user']
        if 'username' in self.scope['url_route']['kwargs']:
            other_username = self.scope['url_route']['kwargs']['username']
            other_user = await self.get_user(other_username)
            self.thread = await self.get_personal_thread([self.user, other_user])
            self.group_name = str(self.thread.id)
        elif 'id' in self.scope['url_route']['kwargs']:
            self.thread = await self.get_thread(self.scope['url_route']['kwargs']['id'])
            self.group_name = self.scope['url_route']['kwargs']['id']

        all_threads = await self.get_all_threads()
        print(all_threads)
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        for thread in all_threads:
            await self.channel_layer.group_add(thread, self.channel_name)

        await self.send({
            'type': 'websocket.accept'
        })
    
    async def websocket_receive(self, event):
        message = json.loads(event['text'])
        msg = message['message']
        print(f'message: {msg}')
        chat_message = await self.create_messsage(self.user, self.thread, msg)
        print(chat_message.id)
        print('event:', event['text'])
        id = chat_message.id
        event_details = json.loads(event['text']) 
        chat_message = event_details['message']
        sender = event_details['sender']
        html_id = event_details['html_id']
        await self.channel_layer.group_send(self.group_name, {
            'type': 'websocket.message',
            'text': json.dumps({
                'id':id,
                'chat_message':chat_message,
                'sender':sender,
                'html_id':html_id,
                'title': event_details['title'],
                'image_url': event_details['image_url']
            })
        })

    async def websocket_disconnect(self, event):
        pass

    async def websocket_message(self, event):
        print(event)
        event_details = json.loads(event['text'])
        print(event_details) 
        # chat_message = event_details['message']
        sender = event_details['sender']
        html_id = event_details['html_id']
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps({
                'id': event_details['id'],
                'chat_message': event_details['chat_message'],
                'sender': sender,
                'html_id': html_id,
                'title': event_details['title'],
                'image_url': event_details['image_url']
            })
        })

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def get_personal_thread(self, users):
        return Thread.objects.get_or_create_personal_thread(users)

    @database_sync_to_async
    def create_messsage(self, sender, thread, message):
        chat_message = ChatMessage.objects.create(sender=sender, thread=thread, message=message)
        thread.save()
        return chat_message

    @database_sync_to_async
    def get_all_threads(self):
        all_threads = [str(thread.id) for thread in self.user.thread_set.all() if thread.id != self.thread.id]
        print(all_threads)
        return all_threads
        
    @database_sync_to_async
    def get_thread(self, id):
        return Thread.objects.get(id=id)


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.user = self.scope['user']
        all_threads = await self.get_all_threads()
        for thread in all_threads:
            await self.channel_layer.group_add(thread, self.channel_name)
    
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        message = json.loads(event['text'])
        msg = message['message']
        print(f'message: {msg}')
        chat_message = await self.create_messsage(self.user, self.thread, msg)
        print(chat_message.id)
        print('event:', event['text'])
        id = chat_message.id
        event_details = json.loads(event['text']) 
        chat_message = event_details['message']
        sender = event_details['sender']
        html_id = event_details['html_id']
        await self.channel_layer.group_send(self.group_name, {
            'type': 'websocket.message',
            'text': json.dumps({
                'id':id,
                'chat_message':chat_message,
                'sender':sender,
                'html_id':html_id,
                'title': event_details['title'],
                'image_url': event_details['image_url']
            })
        })

    async def websocket_disconnect(self, event):
        pass

    async def websocket_message(self, event):
        print(event)
        event_details = json.loads(event['text'])
        print(event_details) 
        # chat_message = event_details['message']
        sender = event_details['sender']
        html_id = event_details['html_id']
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps({
                'id': event_details['id'],
                'chat_message': event_details['chat_message'],
                'sender': sender,
                'html_id': html_id,
                'title': event_details['title'],
                'image_url': event_details['image_url']
            })
        })

    @database_sync_to_async
    def get_all_threads(self):
        all_threads = [str(thread.id) for thread in self.user.thread_set.all()]
        return all_threads

    @database_sync_to_async
    def create_messsage(self, sender, thread, message):
        chat_message = ChatMessage.objects.create(sender=sender, thread=thread, message=message)
        thread.save()
        return chat_message

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)