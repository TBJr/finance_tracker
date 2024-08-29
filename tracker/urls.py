from django.urls import path
from . import views
from .views import export_transactions_pdf, export_transactions_excel

# urlpatterns = [
#     path('register/', views.register, name='register'),
# ]
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('visualize_expenses/', views.visualize_expenses, name='visualize_expenses'),
    path('accounts/profile/', views.profile, name='profile'), # Profile page
    path('export/pdf/', export_transactions_pdf, name='export_transactions_pdf'),
    path('export/excel/', export_transactions_excel, name='export_transactions_excel'),
]
