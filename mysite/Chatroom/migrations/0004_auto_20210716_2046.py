# Generated by Django 3.0.8 on 2021-07-16 12:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Chatroom', '0003_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['time', 'sender', 'group']},
        ),
        migrations.AddField(
            model_name='groups',
            name='last_modified',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
