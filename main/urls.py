from django.conf.urls import url
from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$',views.homepage,name='homepage'),
    url(r'^types/(?P<animal_type>\w+)/$',views.about_type,name='about_type'),
    url(r'^animal/(?P<animal_name>[\w,\s]+)/$',views.about_animal,name='about_animal'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^types/(?P<animal_type>\w+)/add',views.add_animal,name='add_animal')
]