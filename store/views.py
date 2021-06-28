from django.core import paginator
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.http import JsonResponse
from .utils import cookieCart,cartData, guestOrder
from .forms import UserRegisterForm
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from datetime import datetime
from django.views.generic import ListView
import requests

import json
def store(request) :
    data=cartData(request)
    cartItems=data['cartItems']
    
       

    products =Product.objects.all()
    page = request.GET.get('page')
    # a modifier lorque on a plus que 6 products
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
  
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']

    context ={'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store/cart.html',context)


def checkout(request) :
    
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    

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



def viewProduct(request , id):

    if request.user.is_authenticated :
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items=order.order_item_set.all()
        cartItems=order.get_cart_item
    else :
        items=[]
        order ={'get_cart_items': 0 , 'get_cart_total':0}

        cartItems=order['get_cart_items']
    
    product = get_object_or_404(Product,id =id)
    context ={ 'product' : product ,'items':items,'order':order,'cartItems':cartItems}
    return render(request , 'store/viewProduct.html',context)

   



    
    


    
    
def register(request):
    data = cartData(request)    
    cartItems = data['cartItems']
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6LdBaV0bAAAAAFH1DiloL7RWjcqnvsLHu7x4jd3l"
        cap_data={
            "secret" : cap_secret,
            "response" : captcha_token


        }
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        print(cap_server_response)

        if form.is_valid():

            myuser = form.save()
            subject = 'creation de compte'

            message = ( 'hello '+ form.cleaned_data.get('first_name') + ' ' + form.cleaned_data.get('last_name') + ' thank you for signing up to our website  . ' + '\n' +
                        'here are your login     information : ' + '\n' +
                        'username : ' + form.cleaned_data.get('username') + '\n' + 
                        'password : ' + form.cleaned_data.get('password1') ) 


            

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
            p  = Paginator(product,6)
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





