from products.models import ProductCategory, Product
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    context = {
        'title': 'GeekShop',
            }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    context = {'title': 'Geekshop - Каталог', 'categories': ProductCategory.objects.all(), }
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context['products'] = products_paginator
    return render(request, 'products/products.html', context)
