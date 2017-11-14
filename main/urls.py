from django.conf.urls import url
from . import views
app_name = 'main'
urlpatterns = [
    url(r'^$',views.homepage,name='homepage'),
    url(r'^(?P<animal_type>\w+)/(?P<animal_name>\w+)/$',views.about,name='about')
]