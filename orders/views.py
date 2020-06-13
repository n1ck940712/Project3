from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum
import  json
from .models import menuCategory, cart, regularPizza, sicilianPizza, pizzaToppings, dinnerPlatter, salad, pasta, subs, orderList, addOn

superuser = User.objects.filter(is_superuser=True)
if superuser.count() == 0:
    superuser=User.objects.create_user("admin","admin@admin.com","adminadmin")
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.save()

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": "Login first"})
    context = {
    "user": request.user,
    "message": None
    }
    return render(request, "orders/index.html", context)

def loginPage(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message":"Invalid Credentials"})
    return render(request, "orders/login.html", {"message":message})

def logoutPage(request):
    logout(request)
    return render(request, "orders/login.html", {"message":"Successfully logged out."})

def register(request):
    if request.method=="POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        new_user=User.objects.create_user(username,email,password)
        new_user.save()
        return render(request, "orders/login.html", {"message":"Registration successful. You can login now."})
    else:
        return render(request, "orders/login.html")


def orderNow(request):
    category = "Regular Pizza"
    get_order = orderList.objects.all()
    if not get_order:
        order_number=1
        get_order=orderList(ordered_by=request.user, order_number=order_number, order_status="ordering")
        get_order.save()
        order_number=getOrderNum(request)
    else:
        get_order=orderList.objects.filter(ordered_by=request.user, order_status="ordering")
        if not get_order:
            get_order=orderList.objects.order_by("order_number").reverse()[0]
            order_number=getattr(get_order, "order_number")
            order_number+=1
            get_order=orderList(ordered_by=request.user, order_number=order_number, order_status="ordering")
            get_order.save()
            order_number=getOrderNum(request)
        elif get_order:
            order_number=getOrderNum(request)
    print(order_number)
    context = {
    "user": request.user,
    "categoryList":  menuCategory.objects.all(),
    "category": category,
    "addOn": getAddOn(category),
    "menuList": tableLookup(category),
    "userCart": list(cart.objects.filter(order_number=getOrderNum(request)).values()),
    "total": list(cart.objects.filter(order_number=getOrderNum(request)).aggregate(Sum("price")).values())[0]}
    return render(request, "orders/menu.html", context)

def orderConfirm(request):
    confirm_order = orderList.objects.get(ordered_by=request.user, order_status="ordering")
    confirm_order.order_status="Preparing"
    confirm_order.save()
    context={
    "user": request.user,
    "message": "Your order has been submitted."
    }
    return render(request, "orders/index.html", context)

def menu(request, category):
    print(getAddOn(category))
    context = {
    "user": request.user,
    "categoryList": menuCategory.objects.all(),
    "category": category,
    "menuList": tableLookup(category),
    "addOn": getAddOn(category),
    "userCart": list(cart.objects.filter(order_number=getOrderNum(request)).values()),
    "total": list(cart.objects.filter(order_number=getOrderNum(request)).aggregate(Sum("price")).values())[0]}
    return render(request, "orders/menu.html", context)

def addItem(request,category):
    if request.method=="POST":
        name=request.POST["name"]
        price=request.POST["price"]
        size=request.POST["size"]
        if "cheese" in request.POST:
            remark="extra cheese"
        else:
            remark=""
        if category!="Subs":
            topping1=request.POST["topping1"]
            topping2=request.POST["topping2"]
            topping3=request.POST["topping3"]
            userCart=cart(category=category, item=name, price=price, order_number=getOrderNum(request), add_on1=topping1, add_on2=topping2, add_on3=topping3, remark=remark)
        if category=="Subs":
            if "add_on1" not in request.POST:
                add_on1=""
            else:
                add_on1=request.POST["add_on1"]
            if "add_on2" not in request.POST:
                add_on2=""
            else:
                add_on2=request.POST["add_on2"]
            if "add_on3" not in request.POST:
                add_on3=""
            else:
                add_on3=request.POST["add_on3"]
            userCart=cart(category=category, item=name, price=price, order_number=getOrderNum(request), add_on1=add_on1, add_on2=add_on2, add_on3=add_on3, remark=remark)
        userCart.save()
    context = {
        "user": request.user,
        "categoryList": menuCategory.objects.all(),
        "category": category,
        "menuList": tableLookup(category),
        "userCart": list(cart.objects.filter(order_number=getOrderNum(request)).values()),
        "addOn": getAddOn(category),
        "total": list(cart.objects.filter(order_number=getOrderNum(request)).aggregate(Sum("price")).values())[0]
    }
    return render(request, "orders/menu.html", context)

def removeItem(request, category):
    cat = request.POST["category"]
    item = request.POST["item"]
    price = request.POST["price"]
    userCart=cart.objects.filter(category=cat, item=item, price=price, order_number=getOrderNum(request))[0]
    userCart.delete()
    context = {
        "user": request.user,
        "categoryList": menuCategory.objects.all(),
        "category": category,
        "menuList": tableLookup(category),
        "userCart": list(cart.objects.filter(order_number=getOrderNum(request)).values()),
        "addOn": getAddOn(category),
        "total": list(cart.objects.filter(order_number=getOrderNum(request)).aggregate(Sum("price")).values())[0]
    }
    return render(request, "orders/menu.html", context)

def orderManager(request):
    context={
        "order_list": list(orderList.objects.order_by("order_number").reverse().values()),
        "order_cart": list(cart.objects.all().values()),
    }
    return render(request, "orders/manager.html", context)

def orderViewer(request):
    context={
        "order_list": list(orderList.objects.filter(ordered_by=request.user).values()),
        "order_cart": list(cart.objects.all().values()),
    }
    return render(request, "orders/viewer.html", context)

def orderReady(request):
    order_number = request.POST["order_number"]
    order_ready = orderList.objects.get(order_number=order_number)
    order_ready.order_status="Completed"
    order_ready.save()
    context={
        "order_list": orderList.objects.order_by("order_number").reverse(),
        "order_cart": list(cart.objects.all().values()),
    }
    return render(request, "orders/manager.html", context)

def tableLookup(data):
    if data == "Regular Pizza":
        return regularPizza.objects.all()
    if data == "Sicilian Pizza":
        return sicilianPizza.objects.all()
    if data == "Pizza Toppings":
        return list(pizzaToppings.objects.values())
    if data == "Dinner Platter":
        return dinnerPlatter.objects.all()
    if data == "Pasta":
        return pasta.objects.all()
    if data == "Salad":
        return salad.objects.all()
    if data == "Subs":
        return subs.objects.all()
    if data == "addOn":
        return list(addOn.objects.values())

def getOrderNum(request):
    get_order=orderList.objects.get(ordered_by=request.user, order_status="ordering")
    return get_order

def getAddOn(data):
    if "Pizza" in data:
        add_on=tableLookup("Pizza Toppings")
    elif data=="Subs":
        add_on=tableLookup("addOn")
    else:
        add_on=""
    return add_on
