from django.shortcuts import render


def index(request):
    context = { 'title': 'GeekShop - Admin'}
    return render(request, 'admins/index.html', context)
