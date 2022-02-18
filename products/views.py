from products.models import ProductCategory, Product
from django.shortcuts import render


def index(request):
    context = {
        'title': 'GeekShop',
            }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Geekshop - Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }

    return render(request, 'products/products.html', context)
