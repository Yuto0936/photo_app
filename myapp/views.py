from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from .forms import CustomUserCreationForm, PhotoForm, CityForm
from .models import Photo, Category, City
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
import requests
import json



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_username = form.cleaned_data['username']
            input_email = form.cleaned_data['email']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(email=input_email, password=input_password)

            if new_user is not None:
                login(request, new_user)
                return redirect('myapp:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})


def index(request):
    photos = Photo.objects.all().order_by('-created_at')
    url = 'http://api.openweathermap.org/data/2.5/weather?units=metric&q={}&units=imperial&appid=f448c72be27bc84a6cfbbb669228e298'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name'].lower()
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'
        

        if err_msg:
            message = err_msg
            message_class = 'alert-danger'
        else:
            message = 'City added succenssfully!'
            message_class = 'alert-info'

    form = CityForm()
    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    
    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class,
        'photos': photos,
    }
    return render(request, 'myapp/index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('myapp:index')



def users_detail(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    photos = user.photo_set.all().order_by('-created_at')
    return render(request, 'myapp/users_detail.html', {'user': user, 'photos': photos})


@login_required
def photos_new(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, '投稿が完了しました！')
        return redirect('myapp:users_detail', pk=request.user.pk)
    else:
        form = PhotoForm()
    return render(request, 'myapp/photos_new.html', {'form':form})


def photos_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)


    return render(request, 'myapp/photos_detail.html', {'photo': photo})


@require_POST
def photos_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('myapp:users_detail', request.user.id)


@login_required
def edit(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        form = PhotoForm(request.POST,request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('myapp:photos_detail', pk=pk)
    else:
        form = PhotoForm(instance=photo)
    context = {'form': form, 'photo': photo}
    return render(request, 'myapp/edit.html', context)


def photos_category(request, category):
    # titleがURLの文字列と一致するCategoryインスタンスを取得
    category = Category.objects.get(title=category)
    # 取得したCategoryに属するPhoto一覧を取得
    photos = Photo.objects.filter(category=category).order_by('-created_at')
    return render(request, 'myapp/index.html', {'photos': photos, 'category': category})