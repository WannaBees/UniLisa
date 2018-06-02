from django.http import Http404
from django.shortcuts import render

from shopping.forms import SignUpForm
from .models import Item, ShoppingCart

from django.contrib.auth import  authenticate,logout
from django.contrib.auth import login as djangologin
from django.shortcuts import render, redirect
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
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'shopping/index.html', {'subview': 'register','form':form})


def index(request):
    all_items = Item.objects.all()
    searchTerm = request.GET.get("search")

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

    applyFilter = searchTerm is not None and len(searchTerm) > 0

    loggedIn = request.user.is_authenticated
    username = request.user.username
    if applyFilter:
        def filterItemFn(item):
            return searchTerm.lower() in item.item_name.lower()
        all_items = list(filter(filterItemFn,all_items))
        #raise Http404("filtered" + str(len(all_items)))

    return render(request, 'shopping/index.html', {'all_items': all_items,'subview':'overview','applyFilter':applyFilter,'username':username, 'loggedIn': loggedIn })


def getCart(user_name):
    try:
        cart = ShoppingCart.objects.get(user_name=user_name)
    except ShoppingCart.DoesNotExist as e:
        cart = ShoppingCart.objects.create()
        cart.user_name = user_name
        cart.save()


    if cart is None:
        print("hot keine shoppingcart")
    else:
        print("shopping cart exists")

def detail(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        action = request.GET.get('action')
        print("action: "+str(action))
        if action == "addtocart":
            cart = getCart(request.user.username)



    except Item.DoesNotExist:
        raise Http404("This item does not exist. To continue shopping, please go back to the main page!")
    return render(request, 'shopping/index.html', {'item': item,'subview':'detail'})


def login(request):
    return render(request, 'shopping/index.html',{'subview':'login'})





