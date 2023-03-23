# Generated by Django 4.1.7 on 2023-03-22 07:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInteraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, unique=True)),
                ('sub_count', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('unsub_count', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
    ]
