from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Transaction

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='<EMAIL>', password='testpassword')
        self.category = Category.objects.create(name='Food', user=self.user)
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=50.00,
            transaction_type='expense',
            date='2024-08-20'
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.amount, 50.00)
        self.assertEqual(self.transaction.transaction_type, 'expense')
        self.assertEqual(self.transaction.user.username, 'testuser')

    def test_str_representation(self):
        self.assertEqual(str(self.transaction), 'expense - 50.00 on 2024-08-20')