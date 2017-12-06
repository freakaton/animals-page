from django.contrib import admin
from .models import Animal, Type

# Register your models here.

class Admin(admin.ModelAdmin):
    pass
admin.site.register(Animal, Admin)
admin.site.register(Type)