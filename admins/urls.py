from django.urls import path

from admins.views import index

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),

]
