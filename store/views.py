from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
from .utils import cartData, guestOrder
from store.forms import UserRegisterForm

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


    products =Product.objects.all()
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
        return JsonResponse("payment submitted.. ",safe=False)



def viewProduct(request):
    data= json.loads(request.body)
    productId =data['productId']
    action =data['action']
    print('productId',productId)
    print('action',action)

    customer = request.user.customer
    product =Product.objects.get(id=productId)

    return JsonResponse("product",safe=False)
    
def register(request):
    data = cartData(request)    
    cartItems = data['cartItems']
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            myuser = form.save()
            username = form.cleaned_data.get('username')
            Customer.objects.create(user = myuser, name = form.cleaned_data.get('first_name') + ' ' + form.cleaned_data.get('last_name'),email = form.cleaned_data.get('email'))
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html', {'form': form})

def search(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == "POST":
        searched = request.POST.get('searched')

        if  searched :
            product = Product.objects.filter(name__contains=searched)
            return render(request,'store/search.html',{'searched' : searched,'products':product, 'cartItems':cartItems})
        else:
            return render(request,'store/search.html',{'searched' : searched,})
    else:
        return render(request,'store/search.html',{})