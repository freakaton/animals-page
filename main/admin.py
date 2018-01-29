from django.contrib import admin
from .models import Animal, Type

# Register your models here.


def verify(modeladmin, request, queryset):
    for model in queryset:
        model.verified = True
        model.save()


verify.short_description = 'Verify selected models'


class AnimalAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    exclude = ('edit_date',)
    list_filter = ('type', 'verified')
    actions = [verify, ]


admin.site.register(Animal, AnimalAdmin)
admin.site.register(Type)
