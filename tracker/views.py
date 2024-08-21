import base64
from io import BytesIO

import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
from .models import Transaction, Category
from django.db.models import Sum


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('transaction_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'tracker/register.html', {'form': form})


def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'tracker/transaction_list.html', {'transactions': transactions})

def visualize_expenses(request):
    transactions = Transaction.objects.filter(user=request.user, transaction_type='expense')
    categories = [t.category.name for t in transactions]
    amounts = [t.amount for t in transactions]

    plt.figure(figsize=(10, 5))
    plt.bar(categories, amounts)
    plt.xlabel('Category')
    plt.title('Expenses by Category')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    image = base64.b64encode(image_png)
    image = image.decode('utf-8')

    return render(request, 'tracker/visualize.html', {'image': image})

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render (request, 'tracker/add_transaction.html', {'form': form})

# @login_required
def home(request):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]
        income = Transaction.objects.filter(user=request.user, transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expenses = Transaction.objects.filter(user=request.user, transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        savings = income - expenses

        top_categories = (
            Transaction.objects.filter(user=request.user, transaction_type='expense')
            .values('category__name')
            .annotate(total_amount=Sum('amount'))
            .order_by('-total_amount')[:3]
        )

        return render(request, 'tracker/home.html', {
            'transactions': transactions,
            'income': income,
            'expenses': expenses,
            'savings': savings,
            'top_categories': top_categories,
        })
    else:
        return render(request, 'tracker/home.html')