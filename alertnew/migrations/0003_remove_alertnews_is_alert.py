# Generated by Django 4.1.7 on 2023-03-20 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alertnew', '0002_alter_alertnews_reason_not_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertnews',
            name='is_alert',
        ),
    ]