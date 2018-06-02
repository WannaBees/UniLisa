from django.db import models

class Item(models.Model):
    item_name = models.CharField(max_length=1000)
    item_description = models.CharField(max_length=10000)
    category = models.CharField(max_length=1000)
    item_photo = models.ImageField(upload_to='static/shopping/upload')
    price = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=10)
    #thumb = models.ImageField(default='default.png', blank=True)

class ShoppingCart(models.Model):
    user_name = models.CharField(max_length=1000)
    product_id = models.CharField(max_length=1000)
    quantity = models.PositiveIntegerField(default=0)
    # thumb = models.ImageField(default='default.png', blank=True)

    def __str__(self):
        return self.item_name
