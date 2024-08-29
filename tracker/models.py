from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=100, choices=TRANSACTION_TYPE_CHOICES)
    # date = models.DateField()
    date = models.DateField(default=timezone.now)  # Ensure this field is correctly defined
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this line to track creation time

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.date}"

# Signal to create default categories after migrations
@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    categories = ['Groceries', 'Rent', 'Utilities', 'Salary']
    for category in categories:
        Category.objects.get_or_create(name=category)