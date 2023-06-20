from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

from .models import *
from .models import posts as pet
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(pet, PetAdmin)

