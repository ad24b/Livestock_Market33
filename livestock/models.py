from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Livestock(models.Model):
    CATEGORY_CHOICES = (
        ('cow', 'Cow'),
        ('goat', 'Goat'),
        ('sheep', 'Sheep'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    weight = models.FloatField()
    age = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='livestock_images/')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sold_livestock')
    


    def __str__(self):
        return self.name
    

#python manage.py makemigrations
#python manage.py migrate
    