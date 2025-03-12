from django.db import models



class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم المنتج")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="صورة المنتج")

    def __str__(self):
        return self.name
