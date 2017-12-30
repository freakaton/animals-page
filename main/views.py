from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Animal, Type, Post
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def last_animals():
    last_animals = []
    for animal in Animal.objects.order_by('-pub_date')[:5]:
        last_animals.append(animal)
    return last_animals
 
def homepage(request):
    animal_types = []
    user = request.user
    for type in Type.objects.all():
        try:
            type.latest_update = type.animal_set.order_by('-pub_date')[0].pub_date
        except Exception:
            type.latest_update = '-'
        animal_types.append(type)
    return render(request, 'main/main_page.html', {
                                            'types':animal_types,
                                            'last_animals':last_animals(),
                                            })

def about_type(request,animal_type):
    animal_type = Type.objects.get(name=animal_type)
    return render(request,'main/about_type.html',{
                                            'animal_type': animal_type,
                                            'last_animals': last_animals(),
                                            })

def about_animal(request,animal_name):
    error = ''
    animal = Animal.objects.get(name=animal_name)
    posts = Post.objects.filter(where=animal,verified=True)
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_active:
            if len(request.POST['text']) > 10:
                new_post = Post.objects.create(
                                user=request.user,
                                text=request.POST['text'],
                                where=animal)
                new_post.save()
                error = 'ok'
            else:
                error = '2small'
    return render(request,'main/about_animal.html',{
                                                'animal': animal,
                                                'last_animals': last_animals(),
                                                'posts':posts,
                                                'error':error,
                                                    })

def register(request):
    if request.method == 'POST':
        try:
            User.objects.get(username=request.POST['username'])
            return render(request,'main/User/register.html',{'error':'exist'})
        except ObjectDoesNotExist:
            pass
        context = request.POST
        if context['username'] and context['password']:
            user = User.objects.create_user(username = context['username'],
                                            email = context['email'],
                                            password = context['password'])
            user.save()
            return redirect('/')
        else:
            return render(request,'main/User/register.html',{'error':'!full_data'})
    else:
        return render(request,'main/User/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/')
        else:
            return render(request,'main/User/login.html',{'error':'!exist'})
    else:
        return render(request,'main/User/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def profile(request):
    error = ''
    posts = Post.objects.filter(user = request.user)
    if request.user.is_staff:
        posts_to_check = Post.objects.filter(verified = False)
    else:
        posts_to_check = None
    if request.method == 'POST':
        if request.POST['post_id'] and request.POST['desicion']:
            post_id = request.POST['post_id']
            desicion = request.POST['desicion']
            try:
                post = Post.objects.get(pk=post_id)
            except ObjectDoesNotExist:
                return render(request,'main/User/profile.html',{'posts':posts, 'error':'!exist',})
            if desicion == 'apply':
                post.verified = True
                post.save()
            elif desicion == 'decline':
                post.delete()
            else:
                error = '?'
        else:
            error = '!full_data'
    return render(request,'main/User/profile.html',{'posts':posts,
                                                    'posts_to_check':posts_to_check,
                                                    'error':error,
                                                    })