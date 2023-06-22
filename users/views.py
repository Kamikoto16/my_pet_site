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
from .models import Category ,comments ,type_of_animal ,status ,role ,list_role
from .models import posts as pet
import hashlib


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
		toa = type_of_animal.objects.get(id=cat_id)

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