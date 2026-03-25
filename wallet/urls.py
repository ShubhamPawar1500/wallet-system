from django.urls import path
from .views import credit_wallet, debit_wallet, get_balance

urlpatterns = [
    path('admin/wallet/credit', credit_wallet),
    path('admin/wallet/debit', debit_wallet),
    path('wallet/balance', get_balance),
]