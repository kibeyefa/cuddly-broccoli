# Generated by Django 3.2.4 on 2022-10-10 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_thread_empty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='empty',
            field=models.BooleanField(default=True),
        ),
    ]