# Generated by Django 4.2.2 on 2023-06-15 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_pet_id_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('id_pet', models.IntegerField()),
                ('content', models.TextField(blank=True, verbose_name='коммент')),
            ],
        ),
    ]
