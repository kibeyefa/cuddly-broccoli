from django.db import models
from django.db.models.aggregates import Count


class ThreadManager(models.Manager):
    def get_or_create_personal_thread(self, users):
        threads = self.get_queryset().filter(thread_type='personal', users__in=users).distinct()
        threads = threads.annotate(u_count=Count('users')).filter(u_count=2)
        if threads.exists():
            return threads.first()
        else:
            thread = self.create(thread_type='personal')
            for user in users:
                thread.users.add(user)
            thread.save()
            return thread

    def thread_exists(self, user1, user2):
        threads = self.get_queryset().filter(thread_type='personal', users__in=[user1, user2]).distinct()
        threads = threads.annotate(u_count=Count('users')).filter(u_count=2)
        if threads.exists():
            return True
        else:
            return False


    def create_group_thread(self):
        thread = self.create(thread_type='group')
        return thread

    # def add_group_member(self, id, user):
    #     threads = self.get_queryset().filter(thread_type='group', user)
    #     self.save()