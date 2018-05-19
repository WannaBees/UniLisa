from django.http import Http404
from django.shortcuts import render
from .models import Item

def index(request):
    all_items = Item.objects.all()
    return render(request, 'shopping/index.html', {'all_items': all_items,'subview':'overview'})


def detail(request, item_id):


    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404("This item does not exist. To continue shopping, please go back to the main page!")
    return render(request, 'shopping/index.html', {'item': item,'subview':'detail'})

def login(request):
    return render(request, 'shopping/index.html',{'subview':'login'})


