from django.shortcuts import render , redirect
from . models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Category
from . forms import SingUpForm
def home(request):
    all_products = Product.objects.all()

    return render(request,'index.html',{'products':all_products})
def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username , password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'با موفقیت وارد شدید')
            return redirect('home')
        else:
            messages.success(request, 'نام کاربری یا پسورد اشتباه است')
            return redirect('login')
    else:
        return render(request, 'login.html')
def logout_user(request):
    logout(request)
    messages.success(request,('با موفقیت خارج شدید'))
    return redirect('home')

def singup_user(request):
    form=SingUpForm()
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password1=form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            messages.success(request, ('اکانت شما ساخته شده'))
            return redirect('home')
        messages.error(request, 'ثبت نام انجام نشد. لطفا خطاهای فرم را بررسی کنید.')
        return render(request, 'singup.html', {'form': form})
    return render(request, 'singup.html', {'form':form})

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

def category(request, cat):
    try:
        category = Category.objects.get(slug=cat)
        products = Product.objects.filter(category = category)
        return render(request, 'category.html', {'products': products, 'category':category})
    except:
        messages.success(request, 'دسته بندی وجود ندارد')
        return redirect('home')