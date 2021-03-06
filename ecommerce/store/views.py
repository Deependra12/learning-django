from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *

# Create your views here.
def store(request):
    if request.user.is_authenticated:
         customer=request.user.customer
         order, created = Order.objects.get_or_create(customer=customer, complete=False)
         cart_items=order.get_total_item
    else:
        items=[]
        order={'get_cart_total':0,'get_total_item':0,'shipping':'False'}
        cart_items=order['get_total_item']

    products=Product.objects.all()
    context={'products':products,'cart_items':cart_items}
    return render(request,'store/store.html',context)

def cart(request):
    if request.user.is_authenticated:
         customer=request.user.customer
         order, created = Order.objects.get_or_create(customer=customer, complete=False)
         items=order.orderitem_set.all()
         cart_items=order.get_total_item
    else:
        items=[]
        order={'get_cart_total':0,'get_total_item':0,'shipping':'False'}
        cart_items=order['get_total_item']

    context={'items':items,'order':order,'cart_items':cart_items}
    return render(request,'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
         customer=request.user.customer
         order, created = Order.objects.get_or_create(customer=customer, complete=False)
         items=order.orderitem_set.all()
         cart_items=order.get_total_item
    else:
        items=[]
        order={'get_cart_total':0,'get_total_item':0,'shipping':'False'}
        cart_items=order['get_total_item']

    context={'items':items,'order':order,'cart_items':cart_items}
    return render(request,'store/checkout.html',context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
	    customer = request.user.customer
	    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
	    customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    
    order.complete = True
    order.save()

    if order.shipping == True:
	    ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

    return JsonResponse('Payment submitted..', safe=False)



