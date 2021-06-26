from django.core import paginator
from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
from .utils import cartData, guestOrder
from .forms import UserRegisterForm
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from datetime import datetime
from django.views.generic import ListView

import json
def store(request) :
    if request.user.is_authenticated :
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        cartItems = order.get_cart_item
       
    else :
        items=[]
        order ={'get_cart_items': 0 , 'get_cart_total':0}
        cartItems=order['get_cart_items']

    products =Product.objects.all().order_by('?')
    page = request.GET.get('page')
    p  = Paginator(products,2)
    try:
         products = p.page(page)
    except PageNotAnInteger:
         products = p.page(1)
    except EmptyPage:
         products = p.page(paginator.num_pages)
    context ={"products": products,'cartItems':cartItems}



    return render(request, 'store/store.html',context)


def cart(request) :
    if request.user.is_authenticated :
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items=order.order_item_set.all()
        cartItems=order.get_cart_item
    else :
        items=[]
        order ={'get_cart_items': 0 , 'get_cart_total':0}

        cartItems=order['get_cart_items']
    
    context ={'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store/cart.html',context)


def checkout(request) :
    
    if request.user.is_authenticated :
        
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items=order.order_item_set.all()
        cartItems=order.get_cart_item

       
    else :
        items=[]
        order ={'get_cart_items': 0 , 'get_cart_total':0}
        cartItems=order['get_cart_items']
    

    context ={'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store/checkout.html',context)


def updateItem(request):
    data= json.loads(request.body)
    productId =data['productId']
    action =data['action']
    print('productId',productId)
    print('action',action)

    customer = request.user.customer
    product =Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created = Order_Item.objects.get_or_create(order=order,product=product)


    if action == 'add':
        orderItem.quantity=(orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity=(orderItem.quantity -1)

    orderItem.save()
    if orderItem.quantity <=0 :
        orderItem.delete()

    return JsonResponse("item was added",safe=False)




def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    if order.shipping == True:
        ShippingAdress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
		)

    return JsonResponse("payment submitted.. ",safe=False)



def viewProduct(request):
    data= json.loads(request.body)
    productId =data['productId']
    product =Product.objects.get(id=productId)
    


    return render(request,'store/viewProdocut.html',{'product' : product})
    
def register(request):
    data = cartData(request)    
    cartItems = data['cartItems']
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            myuser = form.save()
            subject = 'creation de compte'
            message = ( f'hello '+ form.cleaned_data.get('first_name') + f' ' + form.cleaned_data.get('last_name') +f' thank you for signing up to our website  . ' +  + f'\n' +
                        f'here are your login information : ' + + f'\n' +
                        f'username : ' + form.cleaned_data.get('username') + f'\n' + 
                        f'password : ' + form.cleaned_data.get('password1') ) 

            

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [form.cleaned_data.get('email'), ]
            send_mail( subject, message, email_from, recipient_list )
            username = form.cleaned_data.get('username')
            Customer.objects.create(user = myuser, name = form.cleaned_data.get('first_name') + ' ' + form.cleaned_data.get('last_name'),email = form.cleaned_data.get('email'))
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html', {'form': form})

def search(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == "GET":
        searched = request.GET.get('searched')

        if  searched :
            
            product = Product.objects.filter(name__contains=searched)
            page = request.GET.get('page')
            p  = Paginator(product,2)
            try:
               produit = p.page(page)
            except PageNotAnInteger:
               produit = p.page(1)
            except EmptyPage:
               produit = p.page(paginator.num_pages)


            return render(request,'store/search.html',{'searched' : searched,'products':product, 'cartItems':cartItems,'produit':produit})
        else:
            return render(request,'store/search.html',{'searched' : searched,})
    else:
        return render(request,'store/search.html',{})





