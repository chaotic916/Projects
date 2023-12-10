from django.shortcuts import render, redirect
from django.http import HttpResponse
from item.models import Category, Item
from .forms import SignupForm, LoginForm

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(request, 'mall/index.html',{
        'categories':categories,
        'items':items,
    })

def contact(request):
    return render(request, 'mall/contact.html')

def signup(request):
    # if press the submit button
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'mall/signup.html',{
        'form':form
    })