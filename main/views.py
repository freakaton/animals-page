from django.shortcuts import render
from django.http import HttpResponse
from .models import Animal, Type


# Create your views here.
def last_animals():
    last_animals = []
    for animal in Animal.objects.order_by('-pub_date')[:5]:
        last_animals.append(animal)
    return last_animals
 
def homepage(request):
    animal_types = []
    for type in Type.objects.all():
        type.latest_update = type.animal_set.order_by('-pub_date')[0].pub_date
        animal_types.append(type)
    return render(request, 'main/main_page.html', {
                                            'types':animal_types,
                                            'last_animals':last_animals(),
                                            })

def about_type(request,animal_type):
    animal_type = Type.objects.get(name=animal_type)
    animal_type.get_image = 'images/' + animal_type.name + '.png'
    return render(request,'main/type_about.html',{
                                            'animal_type': animal_type,
                                            'last_animals': last_animals(),
                                            })