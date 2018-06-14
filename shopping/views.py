from functools import reduce


from django.http import Http404, HttpResponseRedirect

from shopping import notifications
from shopping.cart import addToCart, userCartItems
from shopping.forms import SignUpForm, OrderForm
from shopping.view_environment import environment
from .models import Item, ShoppingCart

from django.contrib.auth import  authenticate,logout
from django.contrib.auth import login as djangologin
from django.shortcuts import render
from django.core.mail import send_mail

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
            try:
                addToCart(request.user.username,item,1)
            except:
                return HttpResponseRedirect("/shop/" + str(item_id)+"?notification=outofstock")

            return HttpResponseRedirect("/shop/"+str(item_id))
    except Item.DoesNotExist:
        raise Http404("This item does not exist. To continue shopping, please go back to the main page!")

    site_env = {'item': item,'subview':'detail'}
    env = environment(request, site_env)
    return render(request, 'shopping/index.html', env)




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
            return HttpResponseRedirect("/shop?notification=registered")
    else:
        form = SignUpForm()
    site_env = {'subview': 'register','form':form}
    env = environment(request, site_env)
    return render(request, 'shopping/index.html', env)



def login(request):
    site_env = {'subview':'login'}
    env = environment(request, site_env)
    return render(request, 'shopping/index.html', env)



def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            zip = form.cleaned_data.get('zip')
            street = form.cleaned_data.get('street')
            streetnumber = form.cleaned_data.get('streetnumber')
            city = form.cleaned_data.get('city')
            country = form.cleaned_data.get('country')
            complete_order(request)
            email = request.user.email
            send_mail(
                'Order Confirmation',
                'Dear ' + request.user.username + ' \n\r Thank you for your order.' + '\n\r Your order will be delivered to the following address: \n\r'+str(street)
                + ' ' + str(streetnumber) + '\n\r' + str(city) + ' ' + str(zip) + '\n\r' + country + '\n\r Your UniLIsa-Team ',
                'noreply@huck-it.de',
                [email],
                fail_silently=False,
            )
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


def cart(request):
    user_id = request.user.username
    cartitems = userCartItems(user_id)
    print("has cart items for cart: "+str(len(cartitems)))
    prices = map(lambda item: item.product.price * item.quantity, cartitems)

    if len(cartitems) == 0:
        order_sum = 0
    else:
        order_sum = reduce(lambda x, y: x + y, prices)

    site_env = {'subview': 'cart','cart_items': cartitems,'order_sum': order_sum}
    env = environment(request, site_env)
    return render(request, 'shopping/index.html', env)














