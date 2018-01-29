from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=500, null=True)
    image = models.ImageField(upload_to='types/', null=True, blank=True)

    def __str__(self):
        return self.name

    def my_animals(self):
        animals = self.animal_set.filter(verified=True)
        return animals

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class Animal(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=500, null=True)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(null=True, auto_now=True)
    image = models.ImageField(upload_to='animales/', null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Post (models.Model):
    user = models.ForeignKey(User, verbose_name='Author')
    text = models.CharField(max_length=10000)
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(null=True, auto_now=True)
    verified = models.BooleanField(default=False)
    where = models.ForeignKey(Animal)

    def __str__(self):
        return 'post at animal ' + str(self.where)
