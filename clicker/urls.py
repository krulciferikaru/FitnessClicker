from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_view, name='home'),
    path('click/', views.click, name='click'),
    path('reset/', views.reset, name='reset'),
    path('purchase/', views.purchase_upgrade, name='purchase'),
]