from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('Income', 'Income'),
        ('Expense', 'Expense')
    )

    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES
    )
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
        
    def get_expense_total(self, request_user):
        if request_user.is_authenticated:
            return float(Transaction.objects.filter(user=request_user, transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0)
        return 0
    
    def get_income_total(self, request_user):
        if request_user.is_authenticated:
            return float(Transaction.objects.filter(user=request_user, transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0)
        return 0
    
    def get_balance(self, request_user):
        return self.get_income_total(request_user) - self.get_expense_total(request_user)