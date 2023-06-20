from django.contrib.auth.models import AbstractUser
from django.db import models




class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']
class type_of_animal(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="вид")    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'вид'
        verbose_name_plural = 'вид'
        ordering = ['id']

class posts(models.Model):
    id_user = models.IntegerField()
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    additional_information = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")
    type_of_animal = models.ForeignKey('type_of_animal', on_delete=models.PROTECT, verbose_name="вид")



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'pet'
        verbose_name_plural = 'pet'
        ordering = ['id']


class comments(models.Model):
    id_user = models.IntegerField()
    id_pet = models.IntegerField()
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='comments')

    class Meta:
        db_table = "comments"
        ordering = ["-time_create"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"