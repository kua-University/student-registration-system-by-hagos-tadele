import pytest
from unittest.mock import patch, MagicMock
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Profile

@pytest.mark.django_db
class TestPayment:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.profile = Profile.objects.get(user=self.user)
        self.client.login(username='testuser', password='TestPass123!')

    @patch('students.payment.requests.post')
    def test_payment_initialization_success(self, mock_post):
        """Test successful payment initialization"""
        # Mock successful Chapa API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'success',
            'data': {'checkout_url': 'https://checkout.chapa.co/test'}
        }
        mock_post.return_value = mock_response

        response = self.client.post(reverse('initiate_payment'))
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'checkout_url' in data
        
        # Refresh profile from database
        self.profile.refresh_from_db()
        assert self.profile.tx_ref is not None

    @patch('students.payment.requests.post')
    def test_payment_initialization_failure(self, mock_post):
        """Test failed payment initialization"""
        # Mock failed Chapa API response
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'failed'}
        mock_post.return_value = mock_response

        response = self.client.post(reverse('initiate_payment'))
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is False
        assert 'error' in data

    def test_payment_callback_success(self):
        """Test successful payment callback"""
        self.profile.tx_ref = 'test-tx-ref'
        self.profile.save()

        response = self.client.get(reverse('payment_callback'), {
            'tx_ref': 'test-tx-ref',
            'status': 'success'
        })
        
        self.profile.refresh_from_db()
        assert self.profile.payment_status == 'paid'
        assert response.status_code == 302  # Redirect to success page

    def test_payment_callback_failure(self):
        """Test failed payment callback"""
        self.profile.tx_ref = 'test-tx-ref'
        self.profile.save()

        response = self.client.get(reverse('payment_callback'), {
            'tx_ref': 'test-tx-ref',
            'status': 'failed'
        })
        
        self.profile.refresh_from_db()
        assert self.profile.payment_status == 'pending'
        assert response.status_code == 302  # Redirect to home

    def test_duplicate_payment_prevention(self):
        """Test prevention of duplicate payments"""
        self.profile.payment_status = 'paid'
        self.profile.save()

        response = self.client.post(reverse('initiate_payment'))
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is False
        assert 'already been completed' in data['error'] 