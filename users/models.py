from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    was_seller = models.BooleanField(default=False)  # ✅ حقل جديد لتتبع المستخدمين الذين كانوا بائعين
    # الحقول الجديدة للملف الشخصي
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default.jpg')
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)


class SellerRequest(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"طلب بائع من {self.user.username}"

#python3 manage.py makemigrations 
#python3 manage.py migrate
# python3 manage.py runserver
