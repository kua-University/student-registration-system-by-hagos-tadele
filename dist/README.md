# Student Registration System

A Django-based student registration system with integrated payment processing using Chapa payment gateway. The system allows students to register, handles authentication, and manages payment status.

## Features

- User registration and authentication
- Profile management
- Payment integration with Chapa
- Payment status tracking
- Protected routes and security measures

## Technology Stack

- **Python 3.x**
- **Django 5.1.5**
- **MySQL Database**
- **Pytest** for testing
- **Chapa Payment Gateway**

## Project Structure 

student_registration/
├── manage.py # Django's command-line utility
├── student_registration/ # Project configuration
│ ├── settings.py # Project settings
│ └── urls.py # Main URL routing
└── students/ # Main application
├── views.py # View logic
├── models.py # Database models
├── forms.py # Form handling
├── urls.py # App URL routing
└── tests/ # Test files
├── test_payment.py
└── test_registration.py

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd student_registration
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   - Install MySQL if not already installed
   - Create a database named 'student_reg'
   ```sql
   CREATE DATABASE student_reg;
   ```

5. **Environment Configuration**
   - Update database settings in `student_registration/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'student_reg',
           'USER': 'root',
           'PASSWORD': '',  # Your MySQL password
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```
   - Set your Chapa API keys:
   ```python
   CHAPA_API_KEY = 'your-api-key'
   CHAPA_API_URL = 'https://api.chapa.co/v1/transaction/initialize'
   PAYMENT_AMOUNT = '1000'  # Amount in ETB
   PAYMENT_CURRENCY = 'ETB'
   ```

6. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

## Testing

The project uses pytest for testing. There are two main test files:

### Registration Tests (`test_registration.py`)

Tests user registration functionality:

1. `test_registration_success`
   - Verifies successful user registration
   - Checks user creation in database
   - Verifies profile creation
   - Ensures initial payment status is 'pending'

2. `test_registration_duplicate_username`
   - Tests registration with existing username
   - Verifies appropriate error message

3. `test_registration_password_mismatch`
   - Tests registration with mismatched passwords
   - Verifies error message display

4. `test_registration_weak_password`
   - Tests password strength validation
   - Ensures weak passwords are rejected

5. `test_registration_invalid_email`
   - Tests email validation
   - Verifies error message for invalid email format

### Payment Tests (`test_payment.py`)

Tests payment functionality:

1. `test_payment_initialization_success`
   - Tests successful payment initialization
   - Verifies transaction reference generation
   - Checks Chapa API integration

2. `test_payment_initialization_failure`
   - Tests failed payment initialization
   - Verifies error handling

3. `test_payment_callback_success`
   - Tests successful payment callback
   - Verifies payment status update
   - Checks redirect to success page

4. `test_payment_callback_failure`
   - Tests failed payment callback
   - Verifies payment status remains pending
   - Checks error handling

5. `test_duplicate_payment_prevention`
   - Tests prevention of multiple payments
   - Verifies already paid users can't reinitiate payment

### Running Tests

    -To run all tests
```bash
pytest
```
    -Run specific test file
```bash
pytest students/tests/test_registration.py
pytest students/tests/test_payment.py
```

## Security Features

1. **Authentication and Authorization**
   - Login required for sensitive routes
   - Redirect authenticated users from auth pages
   - Protected payment success page

2. **Form Security**
   - CSRF protection
   - Password validation
   - Input sanitization

3. **Payment Security**
   - Transaction reference validation
   - Payment status verification
   - Duplicate payment prevention

## API Integration

### Chapa Payment Gateway

The system integrates with Chapa payment gateway for handling payments:

1. **Payment Initialization**
   - Generates unique transaction reference
   - Sends payment request to Chapa
   - Handles API response

2. **Callback Handling**
   - Verifies payment status
   - Updates user payment status
   - Handles success/failure scenarios

3. **Configuration**
   ```python
   CHAPA_API_KEY = 'your-api-key'
   CHAPA_API_URL = 'https://api.chapa.co/v1/transaction/initialize'
   PAYMENT_AMOUNT = '1000'  # Amount in ETB
   PAYMENT_CURRENCY = 'ETB'
   ```

## User Flow

1. **Registration**
   - User registers with email and password
   - Profile automatically created
   - Redirected to home page

2. **Payment**
   - User initiates payment
   - Redirected to Chapa payment page
   - Payment status updated via callback
   - Success/failure handling

## Common Issues and Solutions

1. **Database Connection Issues**
   - Verify MySQL is running
   - Check database credentials in settings.py
   - Ensure database exists

2. **Migration Issues**
   - Delete migrations and recreate if needed
   - Ensure database is empty before first migration

3. **Payment Integration Issues**
   - Verify Chapa API keys
   - Check network connectivity
   - Verify callback URL configuration

## Development Notes

1. **Adding New Features**
   - Follow Django's MVT pattern
   - Add appropriate tests
   - Update documentation

2. **Testing**
   - Run tests before commits
   - Maintain test coverage
   - Update test cases for new features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

[Your License Here]
