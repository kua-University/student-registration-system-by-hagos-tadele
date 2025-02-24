from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import StudentRegistrationForm
from .models import Profile
from .payment import initialize_payment
import uuid
from .decorators import redirect_authenticated_user

def generate_transaction_reference():
    return str(uuid.uuid4())

@redirect_authenticated_user
def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profile is automatically created via signal
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your payment.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()
    return render(request, 'students/register.html', {'form': form})

@login_required
def home(request):
    return render(request, 'students/home.html')

@login_required
def initiate_payment(request):
    if request.method == 'POST':
        if request.user.profile.payment_status == 'paid':
            return JsonResponse({
                'success': False,
                'error': 'Payment has already been completed'
            })
        
        # Generate tx_ref only when actually initializing payment
        profile = request.user.profile
        profile.tx_ref = generate_transaction_reference()
        profile.save()
        
        result = initialize_payment(request, request.user)
        return JsonResponse(result)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

@login_required
def payment_success(request):
    # Only show success page if user has actually paid
    if request.user.profile.payment_status != 'paid':
        messages.error(request, 'Please complete your payment first.')
        return redirect('home')
    return render(request, 'students/payment_success.html')

@csrf_exempt
@require_http_methods(["GET", "POST", "OPTIONS"])
def payment_callback(request):
    if request.method == "OPTIONS":
        response = HttpResponse()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
        
    # Debug log the incoming data
    print("GET params:", request.GET)
    print("POST params:", request.POST)
    
    # Get the payment details from query parameters or POST data
    # Check all possible parameter names that Chapa might send
    tx_ref = (
        request.GET.get('trx_ref') or 
        request.GET.get('tx_ref') or 
        request.GET.get('transaction_ref') or
        request.POST.get('tx_ref') or 
        request.POST.get('trx_ref') or
        request.POST.get('transaction_ref')
    )
    
    status = (
        request.GET.get('status') or 
        request.GET.get('payment_status') or
        request.POST.get('status') or
        request.POST.get('payment_status')
    )
    
    print(f"Extracted tx_ref: {tx_ref}")
    print(f"Extracted status: {status}")
    
    if not tx_ref or not status:
        messages.error(request, 'Invalid payment response received.')
        return redirect('home')
    
    try:
        # First try to find the profile by tx_ref
        profile = Profile.objects.filter(tx_ref=tx_ref).first()
        
        # If not found by tx_ref, fall back to pending profiles
        if not profile:
            profile = Profile.objects.filter(payment_status='pending').first()
            if profile:
                print(f"Found profile by pending status: {profile.user.username}")
        else:
            print(f"Found profile by tx_ref: {profile.user.username}")
        
        if profile and status.lower() == 'success':
            profile.payment_status = 'paid'
            profile.save()
            print(f"Updated payment status to paid for user: {profile.user.username}")
            
            # If this is a GET request, it's probably the return URL
            if request.method == 'GET':
                return redirect('payment_success')
            else:
                # For POST requests (webhook), just return 200
                return HttpResponse(status=200)
        else:
            print(f"Payment not successful. Status: {status}")
            messages.error(request, 'Payment was not successful. Please try again.')
            return redirect('home')
        
    except Exception as e:
        print(f"Payment callback error: {str(e)}")
        messages.error(request, 'An error occurred processing your payment.')
        return redirect('home') 