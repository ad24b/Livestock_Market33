from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # الحقول الجديدة للملف الشخصي
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default.jpg')
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)

#python3 manage.py makemigrations 
#python3 manage.py migrate
# python3 manage.py runserver
