from django.shortcuts import render
from django.http import HttpResponse
from .models import Animal


# Create your views here.


def homepage(request):
    animals = []
    for animal in Animal.objects.all():
        animal.url = animal.name.replace(' ','_')
        animals.append(animal)
    return render(request, 'main/index.html', {'animals':animals})

def about(request,animal_name,animal_type):
    animal_name = animal_name.replace('_',' ')
    animal = Animal.objects.get(name=animal_name)
    return render(request, 'main/animal_about.html', {
                                            'animal':animal,
                                            'type':animal_type  
                                            })
