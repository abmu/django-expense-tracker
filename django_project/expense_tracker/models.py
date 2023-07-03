from django.db import models
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
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description