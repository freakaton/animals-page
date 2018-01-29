from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Animal, Type, Post
from django.core.exceptions import ObjectDoesNotExist
from main import forms


def last_animals(request):
    """Get last 5 animals, that have been added."""
    last_animals = []
    for animal in Animal.objects.order_by('-pub_date')[:5]:
        last_animals.append(animal)
    return {'last_animals': last_animals}


def homepage(request):
    """Main page of app."""
    animal_types = []
    request.user
    for type in Type.objects.all():
        try:
            type.latest_update = type.animal_set.order_by(
                '-pub_date')[0].pub_date
        except Exception:
            type.latest_update = '-'
        animal_types.append(type)
    return render(request, 'main/main_page.html', {
        'types': animal_types,
    })


def about_type(request, animal_type):
    """Page, that displays info about type and his animals."""
    animal_type = Type.objects.get(name=animal_type)
    return render(request, 'main/about_type.html', {
        'animal_type': animal_type,
    })


def about_animal(request, animal_name):
    """Same as view above, but with animals."""
    animal = Animal.objects.get(name=animal_name)
    posts = Post.objects.filter(where=animal, verified=True)
    if request.method == 'POST':
        form = forms.AddPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.where = animal
            new_post.user = request.user
            new_post.save()
            form.success = True
    else:
        form = forms.AddPostForm
    return render(request, 'main/about_animal.html', {
        'animal': animal,
        'posts': posts,
        'form': form,
    })


def add_animal(request, animal_type):
    """Get form, that allow users make new animal topics."""
    animal_type = get_object_or_404(Type, name=animal_type)
    if request.method == 'POST':
        form = forms.AddAnimalForm(request.POST, request.FILES)
        if form.is_valid():
            new_animal = form.save(commit=False)
            new_animal.type = animal_type
            new_animal.save()
            return redirect('main:about_animal', animal_name=new_animal.name)
    else:
        form = forms.AddAnimalForm
    return render(request, 'main/add_animal.html', {
        'type': animal_type,
        'form': form})


def register(request):
    """Registration form."""
    if request.method == 'POST':
        try:
            User.objects.get(username=request.POST['username'])
            return render(request, 'main/User/register.html', {
                'error': 'exist'
            })
        except ObjectDoesNotExist:
            pass
        context = request.POST
        if context['username'] and context['password']:
            user = User.objects.create_user(username=context['username'],
                                            email=context['email'],
                                            password=context['password'])
            user.save()
            return redirect('/')
        else:
            return render(request, 'main/User/register.html', {
                'error': '!full_data'
            })
    else:
        return render(request, 'main/User/register.html')


def login(request):
    """Login form."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/')
        else:
            return render(request, 'main/User/login.html', {'error': '!exist'})
    else:
        return render(request, 'main/User/login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def profile(request):
    """One page for staff and common users.

    Staff can manage non-verified posts and animal topics Users can see
    their posts and have permission to delete their own posts

    """
    posts = Post.objects.filter(user=request.user)
    if request.user.is_staff:
        posts_to_check = Post.objects.filter(verified=False)
        animals_to_check = Animal.objects.filter(verified=False)
    else:
        posts_to_check = None
        animals_to_check = None

    if request.method == 'POST':
        desicion = request.POST['desicion']
        if request.POST.get('post_id', False):
            post_id = request.POST['post_id']
            post = Post.objects.get(pk=post_id)
            if desicion == 'apply':
                post.verified = True
                post.save()
            elif desicion == 'decline':
                post.delete()
            else:
                raise Http404
        elif request.POST.get('animal_id', False):
            animal_id = request.POST['animal_id']
            animal = Animal.objects.get(pk=animal_id)
            if desicion == 'apply':
                animal.verified = True
                animal.save()
            elif desicion == 'decline':
                animal.delete()
            else:
                raise Http404
    return render(request, 'main/User/profile.html', {
        'posts': posts,
        'posts_to_check': posts_to_check,
        'animals_to_check': animals_to_check,
    })
