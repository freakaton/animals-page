from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=60)
    description_short = models.CharField(max_length=500)
    description = models.CharField(max_length=5000, null=True)
    image = models.ImageField(upload_to='types/',null=True, blank=True)
    def __str__(self):
        return self.name

    def my_animals(self):
        animals = self.animal_set.all()
        return animals

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
    

class Animal(models.Model):

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    name = models.CharField(max_length=60)
    description_short = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=5000, null=True)
    type = models.ForeignKey('Type',on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(null=True, auto_now=True)
    image = models.ImageField(upload_to='animales/',null=True, blank=True)

class Post (models.Model):
    def __str__(self):
        return 'post at animal ' + self.where.get_name()
    user = models.ForeignKey(User)
    text = models.CharField(max_length=10000)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(null=True, auto_now=True)
    verified = models.BooleanField(default=False)
    where = models.ForeignKey(Animal)