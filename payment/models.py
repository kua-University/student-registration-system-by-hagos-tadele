

# Create your models here.
# course_reg_system/payment/models.py

from django.db import models

class Payment(models.Model):
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def amount_value(self):
        return int(self.amount * 100)  # Convert to lowest currency unit (kobo)

