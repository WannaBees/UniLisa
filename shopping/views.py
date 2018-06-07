from functools import reduce
from urllib.parse import urlencode

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from shopping.forms import SignUpForm, OrderForm, OrderModel
from .models import Item, ShoppingCart

from django.contrib.auth import  authenticate,logout
from django.contrib.auth import login as djangologin
from django.shortcuts import render, redirect
from django.core.mail import send_mail


from django.contrib.auth.models import User, AnonymousUser


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            djangologin(request, user)
            #return redirect('index', args=(notification))
            return HttpResponseRedirect("/shop/orderconfirmation")
    else:
        form = SignUpForm()
    site_env = {'subview': 'register','form':form}
    env = environment(request, site_env)
    return render(request, 'shopping/index.html', env)

def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #form.save()
            zip = form.cleaned_data.get('zip')
            complete_order(request)
            email = request.user.email
            send_mail(
                'Order confirmation',
                'Hallo ' + request.user.username + ' \n\r Deine zip ist '+zip,
                'noreply@huck-it.de',
                [email],
                fail_silently=False,
            )
            #return redirect('index', args=(notification))
            return HttpResponseRedirect("/shop/orderconfirmation")
    else:
        form = OrderForm()
    site_env = {'subview': 'order','form':form}
    env = environment(request, site_env)
    return render(request, 'shopping/index.html', env)


def orderconfirmation(request):
    site_env = {'subview': 'orderconfirmation'}
    env = environment(request, site_env)
    return render(request, 'shopping/index.html', env)


def complete_order(request):
    usercartitems = userCartItems(request.user.username)
    for item in usercartitems:
        item.product.stock = item.product.stock - item.quantity
        item.product.save()
        item.delete()





notificationDict = {'registered':'You have successfully signed up!'}

def index(request):

    all_items = Item.objects.all()
    if request.GET.get("action") == "logout":
        logout(request)
    elif request.GET.get("action") == "login":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            djangologin(request,user)
        else:
            print("User is invalid "+str(username)+":"+str(password))

    searchTerm = request.GET.get("search")

    applyFilter = searchTerm is not None and len(searchTerm) > 0

    if applyFilter:
        def filterItemFn(item):
            return searchTerm.lower() in item.item_name.lower()
        all_items = Item.objects.all()
        all_items = list(filter(filterItemFn, all_items))

    site_env = {'subview': 'overview','all_items':all_items,'applyFilter': applyFilter}

    env = environment(request, site_env)

    return render(request,'shopping/index.html',env)



def environment(request,site_env):
    notification = None
    notificationKey = request.GET.get("notification")
    if notificationKey is not None:
        notification = notificationDict[notificationKey]


    loggedIn = request.user.is_authenticated
    username = request.user.username

        # raise Http404("filtered" + str(len(all_items)))

    result = {}
    if loggedIn:
        shoppingCartItemCount = userCartItemCount(username)
        result =   {'username': username,
                       'loggedIn': True, 'shoppingCartItemCount': shoppingCartItemCount, 'notification': notification}
    else:
        result =  { 'username': username,
                       'loggedIn': False, 'notification': notification }

    merged_result = z = {**result, **site_env}

    return merged_result


def cart(request):
    user_id = request.user.username
    cartitems = userCartItems(user_id)
    print("has cart items for cart: "+str(len(cartitems)))
    prices = map(lambda  item: item.product.price * item.quantity, cartitems )
    order_sum = reduce(lambda x,y: x +  y, prices)
    site_env = {'subview': 'cart','cart_items': cartitems,'order_sum': order_sum}
    env = environment(request, site_env)
    return render(request, 'shopping/index.html', env)



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
    print("available are"+str(stock))
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


def detail(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        path = request.get_full_path()
        components = path.split("/")
        action = components[len(components)-1]
        print("action: "+str(action))
        print("add itemID to cart: " + str(item_id))

        if action == "addToCart":
            print("add item to cart: " + str(item.id))
            addToCart(request.user.username,item,1)
            return HttpResponseRedirect("/shop/"+str(item_id))
    except Item.DoesNotExist:
        raise Http404("This item does not exist. To continue shopping, please go back to the main page!")

    site_env = {'item': item,'subview':'detail'}
    env = environment(request, site_env)
    return render(request, 'shopping/index.html', env)



def login(request):
    site_env = {'subview':'login'}
    env = environment(request, site_env)
    return render(request, 'shopping/index.html', env)








