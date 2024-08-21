from django.urls import path
from . import views

# urlpatterns = [
#     path('register/', views.register, name='register'),
# ]
urlpatterns = [
    path('register/', views.register, name='register'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('visualize/', views.visualize_expenses, name='visualize_expenses'),
]
