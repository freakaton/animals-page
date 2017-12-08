from django.contrib import admin
from .models import Animal, Type

# Register your models here.

class AnimalAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    exclude = ('edit_date',)
    list_filter = ('type',)

admin.site.register(Animal,AnimalAdmin)
