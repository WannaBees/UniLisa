from functools import reduce

from django.http import HttpResponseRedirect

from shopping.models import ShoppingCart, Item


def addToCart(user_name,product,quantity = 1):
    availability = checkAvailability(product.id)
    if availability < quantity:
        raise Exception("Out of stock")
    try:
        cartEntries = ShoppingCart.objects.filter(product= product, user_name= user_name)
        if len(cartEntries) == 0:
            raise ShoppingCart.DoesNotExist
        cartEntry = cartEntries[0]
        cartEntry.quantity = quantity + cartEntry.quantity
        cartEntry.save()

    except ShoppingCart.DoesNotExist as e:
        cart = ShoppingCart(product= product, user_name= user_name,quantity=quantity)
        cart.save()

    return HttpResponseRedirect("/shop/"+str(product))



def checkAvailability(product_id):
    #TODO: handle case if product id is not existing
    item = Item.objects.filter(id=product_id)[0]
    stock = item.stock
    reservations = ShoppingCart.objects.filter(product_id=product_id)
    reservationcount = 0
    for reservation in reservations:
        reservationcount += reservation.quantity
    availablequantity = stock - reservationcount
    return availablequantity

def userCartItems(user_id):
    cart_items = ShoppingCart.objects.filter(user_name=user_id)
    return cart_items


def userCartItemCount(user_id):
    itemquantitites = map(lambda  cart : cart.quantity, userCartItems(user_id))
    try:
        cartitemnumber =  reduce(lambda  x,y: x + y ,itemquantitites)
    except:
        cartitemnumber = 0

    return cartitemnumber
