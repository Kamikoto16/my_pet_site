# Generated by Django 4.2.2 on 2023-06-18 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_comments_options_comments_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='type_of_animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Категория')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'вид',
                'verbose_name_plural': 'вид',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='pet',
            name='type_of_animal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='users.type_of_animal', verbose_name='вид'),
            preserve_default=False,
        ),
    ]
