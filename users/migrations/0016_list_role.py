# Generated by Django 4.2.2 on 2023-06-20 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0015_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='list_role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='users.role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_roles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'list role',
                'verbose_name_plural': 'list roles',
                'ordering': ['id'],
            },
        ),
    ]
