from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.loginPage, name="loginPage"),
    path("logout", views.logoutPage, name="logoutPage"),
    path("register", views.register, name="register"),
    path("order", views.orderNow, name="orderNow"),
    path("orderManager", views.orderManager, name="orderManager"),
    path("orderViewer", views.orderViewer, name="orderViewer"),
    path("orderConfirm", views.orderConfirm, name="orderConfirm"),
    path("orderReady", views.orderReady, name="orderReady"),
    path("category/add/<str:category>", views.addItem, name="addItem"),
    path("category/remove/<str:category>", views.removeItem, name="removeItem"),
    path("category/<str:category>", views.menu, name="menu")
]
