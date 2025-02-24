import uuid
import requests
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def initialize_payment(request, user):
    """Initialize payment with Chapa"""
    try:
        # Generate unique transaction reference
        tx_ref = f"tx-{uuid.uuid4().hex[:10]}"
        
        # Store tx_ref in user's profile
        user.profile.tx_ref = tx_ref
        user.profile.save()
        
        # Construct the callback URL (absolute URL)
        callback_url = request.build_absolute_uri(reverse('payment_callback'))
        
        # Prepare the payload
        payload = {
            'amount': settings.PAYMENT_AMOUNT,
            'currency': settings.PAYMENT_CURRENCY,
            'email': user.email,
            'first_name': user.first_name or user.username,
            'last_name': user.last_name or '',
            'tx_ref': tx_ref,
            'callback_url': callback_url,
            'return_url': request.build_absolute_uri(reverse('payment_success')),
            'customization[title]': 'Student Registration Payment',
            'customization[description]': 'Payment for student registration'
        }
        
        # Set up headers with API key
        headers = {
            'Authorization': f'Bearer {settings.CHAPA_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Make request to Chapa API
        response = requests.post(
            settings.CHAPA_API_URL,
            json=payload,
            headers=headers
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        if data.get('status') == 'success':
            return {
                'success': True,
                'checkout_url': data['data']['checkout_url'],
                'tx_ref': tx_ref
            }
        else:
            logger.error(f"Chapa payment initialization failed: {data}")
            return {
                'success': False,
                'error': 'Payment initialization failed'
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to Chapa: {str(e)}")
        return {
            'success': False,
            'error': 'Could not connect to payment service'
        }
    except Exception as e:
        logger.error(f"Unexpected error during payment initialization: {str(e)}")
        return {
            'success': False,
            'error': 'An unexpected error occurred'
        } 