from django.shortcuts import render

# Create your views here.
# course_reg_system/payment/views.py

import requests
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Payment

def initiate_payment(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        
        payment = Payment.objects.create(amount=amount, email=email)
        
        context = {
            'payment': payment,
            'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
            'amount_value': int(float(amount) * 100),  # Convert to kobo (lowest currency unit)
        }
        return render(request, 'payment/make_payment.html', context)

def verify_payment(request, ref):
    url = f"https://api.paystack.co/transaction/verify/{ref}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result['data']['status'] == 'success':
            payment = Payment.objects.get(id=result['data']['id'])
            payment.paid = True
            payment.save()
            return render(request, 'payment/payment_success.html', {'payment': payment})
    
    return render(request, 'payment/payment_failed.html')

