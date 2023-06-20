from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .utils import *
from time import gmtime, strftime
from .models import Category ,comments ,type_of_animal
from .models import posts as pet

def get_post(request, id):
    if request.method == 'POST':
        try:
            id_user = request.user.id
            id_pet = id
            content = request.POST.get('content')
            comments.objects.create(
                id_user=id_user,
                id_pet=id_pet,
                content=content,
                user=request.user,
            )
        except Exception as e:
            print(e)
            return redirect('login')

    petp = pet.objects.get(id=id)
    comments_list = comments.objects.filter(id_pet=id).select_related('user')
    return render(request, 'post.html', {'pets': petp, 'comments_list': comments_list})
@login_required(login_url='/users/login')
def delete_post(request, id):
    # Получаем URL страницы, с которой пришел запрос
    previous_page = request.META.get('HTTP_REFERER')

    try:
        petp = pet.objects.get(id=id, id_user=request.user.id)
        petp.delete()
        if previous_page:
            return redirect(previous_page) # Перенаправляем пользователя на предыдущую страницу
    except pet.DoesNotExist:
        pass
    
    # Если предыдущая страница не определена, перенаправляем пользователя на страницу профиля
    return redirect('profile')

@login_required(login_url='/users/login')
def profile(request):
    user = request.user
    print(user)
    pett = pet.objects.filter(id_user=request.user.id)
    return render(request, 'profile.html', {'user': user, 'pet': pett})
@login_required(login_url='/users/login')
def add_pet(request):
    user_id = request.user.id

    if request.method == 'POST':
        title = request.POST.get('title')
        slug = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
        content = request.POST.get('content')
        photo = request.FILES['photo']
        cat_id = request.POST.get('cat')

        toa_id = request.POST.get('toa')
        cat = Category.objects.get(id=cat_id)
        toa = type_of_animal.objects.get(id=cat_id)

        pett = pet(id_user=user_id,title=title, slug=slug, additional_information=content, photo=photo, category=cat , type_of_animal=toa )
        pett.save()
        return redirect('home')
    else:
        categories = Category.objects.all()
        type_of_animals = type_of_animal.objects.all()
        context = {'categories': categories , 'type_of_animals':type_of_animals}
        return render(request, 'add_pet.html', context)
def pet_list(request):
    pets = pet.objects.all()
    return render(request, 'posts.html', {'persons': pets})
class RegisterUser(DataMixin,  CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

def home(request):
    pets = pet.objects.all().reverse()[:3]
    return render(request, 'home.html', {'persons': pets})    


def search(request):
    if request.method == 'POST':
        categories = Category.objects.all()
        type_of_animals = type_of_animal.objects.all()
        l1 = request.POST.get('list1')
        l2 = request.POST.get('list2')   
        
        print(l1,l2)     
        pets = pet.objects.filter(category=l1,type_of_animal=l2)

        context = {'persons': pets,'categories': categories , 'type_of_animals':type_of_animals}
       
        return render(request, 'search.html', context)
    categories = Category.objects.all()
    type_of_animals = type_of_animal.objects.all()
    pets = pet.objects.all()

    context = {'persons': pets,'categories': categories , 'type_of_animals':type_of_animals}
   
    return render(request, 'search.html', context)
