from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from . forms import OrderForm,CreateUserForm,CustomerForm
from . filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauntheticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
# Create your views here.


@unauntheticated_user
def registerpage(request):
    form=CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user
            )
            messages.success(request,'Account was successfuly created')
            return redirect('login')
    context={'form':form}
    return render (request,'accounts/register.html',context)

@unauntheticated_user
def loginpage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.success(request,'Username or Password is wrong')
    context={}
    return render(request,'accounts/login.html',context)
        


def logoutuser(request):
    logout(request)
    return render (request,'accounts/login.html')

@login_required(login_url='login')
@admin_only
def home(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()
    total_order=orders.count()
    pending=orders.filter(status='pending').count()
    delivered=orders.filter(status='Delivered').count()
    context={'customers':customers,'orders':orders,'total_order':total_order,'pending':pending,'delivered':delivered}
    return render(request,'accounts/dashboard.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders=request.user.customer.order_set.all()
    total_order=orders.count()
    pending=orders.filter(status='pending').count()
    delivered=orders.filter(status='Delivered').count()
    context={'orders':orders,'total_order':total_order,'pending':pending,'delivered':delivered}
    return render(request,'accounts/user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    product=Product.objects.all()
    context={'product':product}
    return render(request,'accounts/products.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)




@login_required(login_url='login')
def customer(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    total=orders.count()
    myfilter=OrderFilter(request.GET,queryset=orders)
    orders=myfilter.qs
    context={'customer':customer,'orders':orders,'total':total,'myfilter':myfilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createorder(request):
    form=OrderForm()
    if request.method=="POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateorder(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    if request.method=="POST":
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteorder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method=="POST":
        order.delete()
        return redirect ('/')
    context={'order':order}  
    return render(request,'accounts/deleteorder.html',context)