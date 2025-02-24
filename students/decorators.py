from django.shortcuts import redirect
from functools import wraps

def redirect_authenticated_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Redirect to home page if user is authenticated
        return view_func(request, *args, **kwargs)
    return wrapper 