from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm, RegisterForm, DocumentForm, ForgotForm, BookingForm
from django.contrib.auth.models import User
from django.urls import reverse

from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm

import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

import asyncio

def index(request):
    
    if request.method == 'POST':
        
        form = BookingForm(request.POST)

        if form.is_valid():
            
            form.save()
            
            return HttpResponseRedirect('booked')
    else:
        form = BookingForm()
        
    return render(request, 'index.html', {'form':form})

def booking(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BookingForm(request.POST)
        
        #start telegram loop
        loop = asyncio.new_event_loop()
        
        asyncio.set_event_loop(loop)
    
        
        if form.is_valid():     
            form.save()
            message = "Client " + form.cleaned_data.get('email_address') + " made a booking of session length " + form.cleaned_data.get('session_length') + "hrs. Phone number is " + form.cleaned_data.get('phone_number')
            response = loop.run_until_complete(
                telegram(message)
            )
            return HttpResponseRedirect('booked')
        
        loop.close()
    else:
        form = BookingForm()       
        
    return render(request, 'booking.html', {'form': form})
    
async def telegram(text):
    #Telegram Code
    client = TelegramClient('session', settings.API_ID, settings.API_HASH)

    await client.connect()
    
    if not await client.is_user_authorized():
        await client.send_code_request(settings.PHONE)
        await client.sign_in(settings.PHONE, input('Enter the code: '))
    try:
        me = await client.get_me()
        receiver = InputPeerUser(me.id, me.access_hash)
        await client.send_message(receiver, text, parse_mode='html')
    except Exception as e:
        print(e);
    await client.disconnect()
    
     
def booked(request):
    return render(request, 'booked.html')
    

@csrf_exempt
def login_form(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = request.POST['username']
            
            password = request.POST['password']
            
            user = authenticate(request, username = username, password = password)
            
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
                
            else:
                pass

    else:
        form = UserForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    
    return HttpResponseRedirect("/login")

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = request.POST['username']
            
            password = request.POST['password']
            
            first_name = request.POST['first_name']
            
            last_name = request.POST['last_name']
            
            email_address = request.POST["email_address"]
            
            register = User.objects.create_user(username, email_address, password)
            
            register.first_name = first_name
            
            register.last_name = last_name
            
            register.save()
            
            user = authenticate(request, username = username, password = password)
            
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/index')
                
            else:
                return HttpResponse("/register")
    else:
        form = RegisterForm()
        
    return render(request, 'registration/register.html', {'form': form})

def emailconfirmation(request):
    
    return render(request, 'auth/emailconfirmation.html')


@csrf_exempt
def forgotpassword(request):
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ForgotForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = request.POST['username']
            
            # user = authenticate(request, username = username, password = password)
            
            # if user is not None:
            #     login(request, user)
            #     return HttpResponseRedirect('/')
                
            # else:
            #     pass

    else:
        form = ForgotForm()
    
    return render(request, 'registration/forgotpassword.html', {'form': form})
    
def process_payment(request):
    order_id = 6 #request.session.get('order_id')
    
    order = "Rereeee"#get_object_or_404(Order, id=order_id)
    
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': "25.00",
        'item_name': 'Order {}'.format(order_id),
        'invoice': order_id,
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }
    
    form = PayPalPaymentsForm(initial=paypal_dict)
    
    return render(request, 'payments/process_payment.html', {'order': order, 'form': form})

@csrf_exempt
def payment_done(request):
    return render(request, 'payments/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payments/payment_cancelled.html')


@login_required
def videoupload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = DocumentForm()
    
    return render(request, 'videoupload.html', {'form':form})
