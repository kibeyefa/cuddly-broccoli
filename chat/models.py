from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.fields import RandomCharField
from uuid import uuid4

from .managers import ThreadManager
# Create your models here.

User = get_user_model()


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(auto_now=True)


class Thread(models.Model):
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group')
    )

    id = models.UUIDField(default=uuid4, unique=True,
                          editable=False, primary_key=True)
    html_id = RandomCharField(length=10)
    users = models.ManyToManyField(User)
    thread_type = models.CharField(max_length=40, choices=THREAD_TYPE)
    last_activity = models.DateTimeField(auto_now=True)
    objects = ThreadManager()
    empty = models.BooleanField(default=True)

    def __str__(self):
        if self.thread_type == 'personal':
            return f'chat between {self.users.first().username} and {self.users.last().username}'
        return "Group chat " + str(self.id)

    @property
    def thread_name(self):
        return "chatroom_{}".format(self.id)

    @property
    def messages_count(self):
        messages = self.chatmessage_set.all()
        return len(messages)

    # def create_group_pr

    def add_group_member(self, user):
        if self.thread_type == 'group':
            if user not in self.users.all():
                self.users.add(user)
        self.save()

    def remove_group_member(self, user):
        if self.thread_type == 'group':
            if user in self.users.all():
                self.users.remove(user)
        self.save()

    class Meta:
        ordering = ['-last_activity']
