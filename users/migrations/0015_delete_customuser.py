# Generated by Django 4.2.2 on 2023-06-20 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
