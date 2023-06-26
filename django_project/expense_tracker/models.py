from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Purchase(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name