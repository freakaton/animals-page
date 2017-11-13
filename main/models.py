from django.db import models

# Create your models here.


class Animal(models.Model):
    def __str__(self):
        return self.name

    TYPES = (
        ('GR','Грызун'),
        ('PT','Птица'),
        ('KO','Кошка'),
        ('SO','Собака'),
    )
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=2, choices=TYPES)