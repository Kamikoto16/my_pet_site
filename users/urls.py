from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import pet_list ,RegisterUser ,logout_user ,add_pet ,profile,delete_post,get_post,search ,menadje



urlpatterns = [
    path('', include('django.contrib.auth.urls')),
   
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('posts', pet_list, name='pet_list'),
    path('search', search, name='search'),
    path('add_pet', add_pet, name='add_pet'),
    path('deletepost/<int:id>/', delete_post, name='delete_post'),
    path('get_post/<int:id>/', get_post, name='get_post'),



    path('menadje', menadje, name='menadje'),
    
]
