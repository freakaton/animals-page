from django.shortcuts import render
from django.http import HttpResponse
from .models import Animal


# Create your views here.


def homepage(request):
    animals = []
    for animal in Animal.objects.all():
        animals.append(animal)
    return render(request, 'main/index.html', {'animals':animals})

def animal_about(request,animal_id):
    animal = Animal.objects.get(pk=animal_id)
    return render(request, 'main/animal_about.html', {'animal':animal})
