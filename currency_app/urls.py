from django.urls import path

from .views import *
urlpatterns = [
    path('exchange/', exchange, name='exchange'),

]
