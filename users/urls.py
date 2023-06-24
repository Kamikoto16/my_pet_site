from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import pet_list ,RegisterUser ,logout_user ,add_pet ,archive,\
profile,delete_post,get_post,search ,menadje ,admin,delete_user, \
help_view,delete_cooment,change_password,admin_change_password




urlpatterns = [
    path('', include('django.contrib.auth.urls')),
   
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('posts', pet_list, name='pet_list'),
    path('archive', archive, name='archive'),

    path('search', search, name='search'),
    path('add_pet', add_pet, name='add_pet'),
    path('deletepost/<int:id>/', delete_post, name='delete_post'),
    path('get_post/<int:id>/', get_post, name='get_post'),
    path('delete_user/<int:id>/', delete_user, name='delete_user'),
    path('admin_change_password/<int:user_id>/', admin_change_password, name='admin_change_password'),


    path('change_password', change_password, name='change_password'),


    path('admin', admin, name='admin'),
    path('menadje', menadje, name='menadje'),
    path('delete_cooment/<int:id>/', delete_cooment, name='delete_cooment'),

    
    path('help', help_view, name='help'),
    
]
