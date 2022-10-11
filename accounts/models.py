from django.db import models
from chat.models import Thread
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


def get_image_file_path(self, filename):
    return f'{self.user.username}/{"profile-image.png"}'


def get_group_image_file_path(self, filename):
    return f'Group_{self.thread.html_id}/{"icon.png"}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='/group-chat-icon.jpg', upload_to=get_image_file_path)


class GroupProfile(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    admins = models.ManyToManyField(User, related_name='admins')
    image = models.ImageField(
        default='/group-chat-icon.jpg', upload_to=get_group_image_file_path)
    thread = models.OneToOneField(Thread, on_delete=models.SET_NULL, null=True)
