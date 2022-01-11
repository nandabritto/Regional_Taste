from django.db import models


class Product(models.Model):
    boxname = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(null=True)
    product_option1 = models.ImageField(null=True)
    product_option2 = models.ImageField(null=True)

