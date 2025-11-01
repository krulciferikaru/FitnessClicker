from django.urls import path
from . import views

urlpatterns = [
    path("", views.welcome_view, name="welcome"),
    path("index/", views.game_view, name="index"),
    path("click/", views.click, name="click"),
    path("reset/", views.reset, name="reset"),
    path('purchase_upgrade/', views.purchase_upgrade, name='purchase_upgrade'),
    path("prestige/", views.prestige, name="prestige"),
]
