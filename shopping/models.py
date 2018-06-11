from django.db import models

class Item(models.Model):
    item_name = models.CharField(max_length=1000)
    item_description = models.CharField(max_length=10000)
    category = models.CharField(max_length=1000)
    item_photo = models.ImageField(upload_to='static/shopping/upload')
    price = models.PositiveIntegerField(default = 10 )
    stock = models.PositiveIntegerField(default=10)

class ShoppingCart(models.Model):
    user_name = models.CharField(max_length=1000)
    product = models.ForeignKey(
        Item
        , on_delete=models.CASCADE,null=True)

    quantity = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.item_name


