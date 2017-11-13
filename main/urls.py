from django.conf.urls import url
from . import views
app_name = 'main'
urlpatterns = [
    url(r'^$',views.homepage,name='homepage'),
    url(r'^animals/(?P<animal_id>[0-9]+)/$',views.animal_about,name='animal_about')
]