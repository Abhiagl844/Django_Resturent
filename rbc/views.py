from django.shortcuts import render , redirect
from django.http import HttpResponse

from .models import food , Review , user_details
from itemCart.models import cartSes , order1 , orderedItems
from .forms import foodForm , user_detailsForm

from . import machine

from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def home(req):
    choice = food.course_choice
    rate = Review.objects.all()
    q = req.GET.get('q') if req.GET.get('q') != None else ''
    item = food.objects.filter(Q(course__icontains = q))
    
    l = machine.seggestions(req)
    
    context = {"food" : item , "course" : choice , "rate" : rate , 'l' : l}
    return render(req,'home.html',context)

def loginPage(req):
    page = 'login'
    if(req.user.is_authenticated):
        return redirect('home')
    if(req.method == "POST"):
        username = req.POST.get('username').lower()
        password = req.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(req , 'User does not exist!')
        user1 = authenticate(req , username = username , password = password)
        if user1 is not None:
            login(req , user1)
            if user1.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('home')
        else:
            messages.error(req, 'Username or Password is not correct!')
    return render(req,'login-register.html',{'page':page})

def logoutPage(req):
    logout(req)
    return redirect('home')

def registerPage(req):
    page = 'register'
    form = UserCreationForm()
    if(req.method == "POST"):
        form = UserCreationForm(req.POST)
        if(form.is_valid):
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(req , user)
            cartSes(
                user = user
            ).save()
            user_new = user_details.objects.create(
                user = req.user,
                email = "",
                phone = 0,
                address = ""
            )
            user_new.save()
            return redirect('user_details_form')
        else:
            messages.error(req , 'An error occured while Registration!')
    return render(req , 'login-register.html',{'form':form,'page':page})

def user_deltail_Form(req):
    user_for_det = user_details.objects.get(user = req.user)
    userForm = user_detailsForm(instance = user_for_det)


    if(req.method == 'POST'):
        userForm = user_detailsForm(req.POST , instance = user_for_det)
        if(userForm.is_valid()):
            userForm.save()
            return redirect('home')
        else:
            return redirect('user_details_form')
    context = {'userForm' : userForm}
    return render(req , 'user_details_register.html' , context)

def dashPage(req):
    if not req.user.is_superuser:
        return redirect('home')
    rev = Review.objects.all()
    choice = food.course_choice
    orders = order1.objects.all()
    order_items = orderedItems.objects.all()
    q = req.GET.get('q') if req.GET.get('q') != None else ''
    
    order_count = 0
    for order in orders:
        if order.status != "Delivered" or order.status != "Canceled":
            order_count += 1

    if q == "Menu":
        item = food.objects.all()
    else:
        item = food.objects.filter(Q(course__icontains = q))
    context = {"food" : item , "course" : choice , "rev" : rev , "q" : q , "orders":orders , "order_items" : order_items , "order_count":order_count}
    return render(req , 'dashboard.html' , context)

def menuCreation(req):
    menuForm = foodForm()
    if(req.method == "POST"):
        menuForm = foodForm(req.POST , req.FILES)
        if(menuForm.is_valid()):
            menuForm.save()
        return redirect('dashboard')
    context = {'menuForm' : menuForm}
    return render(req , 'menuCRUD.html',context)

def menuUpdation(req , pk):
    item = food.objects.get(id = pk)
    menuForm = foodForm(instance = item)

    if(req.method == "POST"):
        menuForm = foodForm(req.POST , req.FILES , instance=item)
        if menuForm.is_valid():
            menuForm.save()
            return redirect("dashboard")
    context = {"menuForm" : menuForm}
    return render(req , 'menuCRUD.html' , context)

def menuDeletion(req , pk):
    item = food.objects.get(id = pk)
    if(req.method == "POST"):
        item.delete()
        return redirect('dashboard')
    return render(req , 'delete.html')


def foodPage(req , pk):
    items = food.objects.get(id = pk)
    rev =  Review.objects.filter(food = items)
    if(req.user.is_authenticated):
        user1 = req.user
    else:
        user1 = User.objects.get(username='anonymous')
    if(req.method == "POST"):
        review = Review.objects.create(
            user = user1,
            food = items,
            body = req.POST.get('body'),
            rating = req.POST.get('rating')
        )
        return redirect('foodPage',pk=items.id)
    
    context={'items' : items , 'rev' : rev}
    return render(req , 'food.html' , context)

def user_orders(req):
    orders = order1.objects.filter(user = req.user)
    orderItems = orderedItems.objects.filter(order__in = orders)
    q = req.GET.get('q') if req.GET.get('q') != None else ''
    if q != "":
        canOrder = order1.objects.get(id = q)
        canOrder.status = 'Canceled'
        canOrder.save()
    context = {'orders' : orders , 'orderItems' : orderItems}
    return render(req , 'userOrders.html' , context)