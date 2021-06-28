from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True,unique=True)

    def __str__(self):
        return self.name or ''


class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=7 , decimal_places=2)
    
    image = models.ImageField(null=True,blank=True)
    detail =models.TextField(null=True)

    def __str__(self):
        return self.name or ''

    @property
    def imageURL(self):
        try :
            url=self.image.url
        except :
            url=''    
        return url



class ProductImage(models.Model) :
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
         return self.product.name  

    @property
    def imageURL(self):
        try :
            url=self.image.url
        except :
            url=''    
        return url 

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered= models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)


    def __str__(self):
        return self.transaction_id or ''

    @property
    def get_cart_total(self):
        orderitems=self.order_item_set.all()    
        total = sum([item.get_total for item in orderitems ])
        return total
    @property
    def shipping(self):
        shipping = False
        orderitems = self.order_item_set.all()
        for i in orderitems:
            shipping = True
        return shipping

    @property
    def get_cart_item(self):
         orderitems=self.order_item_set.all()
         total = sum([item.quantity for item in orderitems])
         return total   

class Order_Item(models.Model):
    product =models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True)
    order =models.ForeignKey(Order, on_delete=models.SET_NULL,null=True,blank=True)
    quantity =models.IntegerField(default=0,null=True,blank=True)
    date_added= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name or ''

    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total    

class ShippingAdress(models.Model):
        customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True,blank=True)
        order =models.ForeignKey(Order, on_delete=models.SET_NULL,null=True,blank=True)
        address = models.CharField(max_length=200,null=True)
        city = models.CharField(max_length=200,null=True)
        state = models.CharField(max_length=200,null=True)
        zipcode = models.CharField(max_length=200,null=True)
        date_added= models.DateTimeField(auto_now_add=True)



        def __str__(self):
            return self.address or ''


 

