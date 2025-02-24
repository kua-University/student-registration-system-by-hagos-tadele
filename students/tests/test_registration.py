import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Profile

@pytest.mark.django_db
class TestRegistration:
    def setup_method(self):
        print("\nSetting up test...")
        self.client = Client()
        self.register_url = reverse('register')
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        print("Setup complete")

    def test_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_data)
        assert response.status_code == 302  # Redirect after success
        assert User.objects.filter(username='testuser').exists()
        assert Profile.objects.filter(user__username='testuser').exists()
        assert Profile.objects.get(user__username='testuser').payment_status == 'pending'

    def test_registration_duplicate_username(self):
        """Test registration with existing username"""
        User.objects.create_user(username='testuser', password='TestPass123!')
        response = self.client.post(self.register_url, self.valid_data)
        assert response.status_code == 200  # Return to form
        assert 'username already exists' in str(response.content).lower()

    def test_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        data = self.valid_data.copy()
        data['password2'] = 'DifferentPass123!'
        response = self.client.post(self.register_url, data)
        assert response.status_code == 200
        # Look for Django's default error message
        assert "password fields didn" in str(response.content).lower()  # More flexible matching

    def test_registration_weak_password(self):
        """Test registration with weak password"""
        data = self.valid_data.copy()
        data['password1'] = data['password2'] = '123'
        response = self.client.post(self.register_url, data)
        assert response.status_code == 200
        assert 'password is too short' in str(response.content).lower()

    def test_registration_invalid_email(self):
        """Test registration with invalid email"""
        data = self.valid_data.copy()
        data['email'] = 'invalid-email'
        response = self.client.post(self.register_url, data)
        assert response.status_code == 200
        assert 'enter a valid email' in str(response.content).lower() 