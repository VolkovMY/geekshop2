from products.models import ProductCategory, Product
from django.shortcuts import render


def index(request):
    context = {
        'title': 'GeekShop',
            }
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    context = {'title': 'Geekshop - Каталог', 'categories': ProductCategory.objects.all(), }
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    context['products'] = products
    return render(request, 'products/products.html', context)
