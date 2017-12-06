from django.conf.urls import url
from . import views
app_name = 'main'
urlpatterns = [
    url(r'^$',views.homepage,name='homepage'),
    url(r'^(?P<animal_type>\w+)/$',views.about_type,name='about_type'),
    url(r'^(?P<animal_type>\w+)/(?P<animal_name>[\w,\s]+)/$',views.about_animal,name='about_animal'),
]