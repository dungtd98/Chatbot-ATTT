# Generated by Django 4.1.7 on 2023-03-20 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertnew', '0004_alertnews_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertnews',
            name='is_send',
        ),
    ]
