from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
import random
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from .utils import *
from time import gmtime, strftime
from .models import Category ,comments ,type_of_animal ,status ,role ,list_role
from .models import role as roler 
from .models import posts as pet 
from collections import defaultdict
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ChangePasswordForm
import smtplib
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import random
from datetime import datetime, timedelta
from django.utils import timezone





def archive_old_posts():
	print('sss')
	# Вычисляем время месяц назад от текущего времени
	month_ago = timezone.now() - timedelta(days=30)
	# Получаем все записи, у которых время обновления больше месяца назад
	old_posts = posts.objects.filter(time_update__lt=month_ago)
	# Обновляем статус на 'архивный' для всех найденных записей
	status_id = status.objects.get(name='архив').id
	old_posts.update(status_id=status_id)
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
	
	if str(petp.status) == 'архив':
		print(22)
		a =1
	else:
		a =0
	return render(request, 'post.html', {'pets': petp, 'comments_list': comments_list ,'a':a})


from django.utils import timezone

import os
from django.conf import settings

@login_required(login_url='/users/login')
def delete_post(request, id):
    # Получаем URL страницы, с которой пришел запрос
    previous_page = request.META.get('HTTP_REFERER')

    try:
        petp = posts.objects.get(id=id)
        # Удаляем связанный файл из локальных файлов проекта
        file_path = os.path.join(settings.MEDIA_ROOT, str(petp.photo))
        os.remove(file_path)
        petp.delete()
        
        if previous_page:
            return redirect(previous_page)  # Перенаправляем пользователя на предыдущую страницу
    except Exception as e:
        print(e)
        pass
    
    # Если предыдущая страница не определена, перенаправляем пользователя на страницу профиля
    return redirect('profile')

@login_required(login_url='/users/login')
def profile(request):
	user = request.user
	
	pett = pet.objects.filter(id_user=request.user.id , status__name='публично')
	rew = pet.objects.filter(id_user=request.user.id , status__name='проверка')
	archive = pet.objects.filter(id_user=request.user.id , status__name='архив')
	return render(request, 'profile.html', {'user': user, 'pet': pett ,'rew':rew ,'archive':archive})

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
		toa = type_of_animal.objects.get(id=toa_id)

		start_staus = status.objects.get(name="проверка")
	

		pett = pet(id_user=user_id,title=title, slug=slug,status=start_staus, additional_information=content, photo=photo, category=cat , type_of_animal=toa )
		pett.save()
		return redirect('home')
	else:
		categories = Category.objects.all()
		type_of_animals = type_of_animal.objects.all()
		context = {'categories': categories , 'type_of_animals':type_of_animals}
		return render(request, 'add_pet.html', context)
def pet_list(request):
	# check_post_status()
	pets = pet.objects.filter(status__name='публично').order_by('-id')
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
class LoginUser(DataMixin, LoginView ):
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
	archive_old_posts()
	if request.user.id!=None:
		r = request.user.id
		
		# pett = list_role(role_id=role.objects.get(name='пользователь'),user_id=request. )
  # Укажите имя пользователя, для которого вы хотите создать запись

		if  list_role.objects.filter(user=request.user.id).exists():
			request.session['role'] = str(list_role.objects.get(user=r).role)
		# pett.save()

	pets = pet.objects.filter(status__name='публично').order_by('-id')[:3]
	return render(request, 'home.html', {'persons': pets})    


def search(request):
	if request.method == 'POST':
		categories = Category.objects.all()
		type_of_animals = type_of_animal.objects.all()
		l1 = request.POST.get('list1')
		l2 = request.POST.get('list2')   
		
		print(l1,l2)     
		pets = pet.objects.filter(category=l1,type_of_animal=l2 ,status__name='публично')

		context = {'persons': pets,'categories': categories , 'type_of_animals':type_of_animals}
	   
		return render(request, 'search.html', context)
	categories = Category.objects.all()
	type_of_animals = type_of_animal.objects.all()
	pets = pet.objects.filter(status__name='публично').order_by('-id')

	context = {'persons': pets,'categories': categories , 'type_of_animals':type_of_animals}
   
	return render(request, 'search.html', context)


def menadje(request):
	if request.method == 'POST':
		print(request.POST.get('fixed_value') , request.POST.get('toa'))

		obj = pet.objects.get(id=request.POST.get('fixed_value'))
		obj.status = status.objects.get(id=request.POST.get('toa'))
		obj.save()
	rew = pet.objects.filter( status__name='проверка')
	pub = pet.objects.filter( status__name='публично')
	archive = pet.objects.filter( status__name='архив')

	statuss = status.objects.all()
	context = {'rew':rew ,'status':statuss ,'archive':archive,'pub':pub}
	return render(request, 'menadje.html', context)

def archive(request):
	pets = pet.objects.filter(status__name='архив').order_by('-id')
	return render(request, 'posts.html', {'persons': pets})


def admin(request):
	if request.method == 'POST':


		user = User.objects.get(id=request.POST.get('fixed_value'))
		role_set = request.POST.get('toa')

		try:
			obj = list_role.objects.get(user_id=user)
			obj.role_id = roler.objects.get(id=role_set)
			obj.save()
		except Exception as e:
			print(e)
			rr = roler.objects.get(id=role_set)
			obj = list_role(user=user,role=rr)
			obj.save()
		# obj.status = status.objects.get(id=request.POST.get('toa'))
		# obj.save()

	
	user_roles_dict = {}
	for user in User.objects.all():
		roles = user.list_roles.all()
		if roles.exists():
			user_roles_dict[user.id] = {"username": user.username, "email": user.email, "role": ""}
			for role in roles:
				user_roles_dict[user.id]["role"] += role.role.name + " "
		else:
			user_roles_dict[user.id] = {"username": user.username, "email": user.email, "role": "пользователь"}
	
	roles = roler.objects.all()
	context = {'user_roles_dict': user_roles_dict,'roles':roles}
	return render(request, 'admin.html', context)   
def delete_user(request, id):
	# Получаем URL страницы, с которой пришел запрос
	previous_page = request.META.get('HTTP_REFERER')

	try:
		u = User.objects.get(id=id)
		u.delete()
		if previous_page:
			return redirect(previous_page) # Перенаправляем пользователя на предыдущую страницу
	except Exception as e:

		pass
	
	# Если предыдущая страница не определена, перенаправляем пользователя на страницу профиля
	return redirect('/users/admin')

def help_view(request):
	captcha_value = random.randint(0,99999999)
	if request.method == 'POST':


		if (str(request.POST.get('captcha_value')) == str(request.POST.get('captcha_value_new'))):

			problem_text = request.POST.get('problem_text')
			email = request.POST.get('email')

			# Отправка письма на почту администратора
			subject = 'Новое сообщение о проблеме'
			message = f'Проблема: {problem_text}\nEmail: {email}'
			from_email = settings.EMAIL_HOST_USER
			to_email = ['gusymba14@gmail.com']  # Замените на вашу почту администратора
			send_mail(subject, message, from_email, to_email)

			messages.success(request, 'Сообщение отправлено администратору')
			return redirect('help')  # Перенаправление на страницу помощи
		else:
			messages.success(request, 'капча не пройдена')
			return redirect('help')  # Перенаправление на страницу помощи			
	context = {'captcha_value' :captcha_value}
	return render(request, 'help.html' , context)

def delete_cooment(request, id):
	# Получаем URL страницы, с которой пришел запрос
	previous_page = request.META.get('HTTP_REFERER')

	try:
		u = comments.objects.get(id=id)
		u.delete()
		if previous_page:
			return redirect(previous_page) # Перенаправляем пользователя на предыдущую страницу
	except Exception as e:

		pass
	
	# Если предыдущая страница не определена, перенаправляем пользователя на страницу профиля
	return redirect('/')
@login_required
def change_password(request):
	if request.method == 'POST':
		form = ChangePasswordForm(request.user, request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password1')
			request.user.set_password(new_password)
			request.user.save()
			messages.success(request, 'Пароль успешно изменён!')
			return redirect('home')
	else:
		form = ChangePasswordForm(request.user)
	return render(request, 'change_password.html', {'form': form})



def admin_change_password(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	form = AdminPasswordChangeForm(user=user, data=request.POST or None)

	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Пароль был успешно изменен')
		return redirect('/users/admin')


	return render(request, 'admin_change_password.html', {'form': form ,'a':user})
	
def your_view(request):
	captcha_value = random.randint(1000, 9999)
	return render(request, 'help.html', {'captcha_value': captcha_value})
    
