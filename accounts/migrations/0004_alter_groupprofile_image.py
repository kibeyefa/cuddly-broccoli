# Generated by Django 3.2.4 on 2022-10-08 13:00

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupprofile',
            name='image',
            field=models.ImageField(default='/group-chat-icon.jpg', upload_to=accounts.models.get_group_image_file_path),
        ),
    ]