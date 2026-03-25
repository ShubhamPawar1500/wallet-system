from django.shortcuts import render
from decimal import Decimal

from django.db import transaction
from django.db.models import F

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Wallet, Transaction
from .permissions import IsAdminUserCustom
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAdminUserCustom])
def credit_wallet(request):
    user_id = request.data.get("user_id")
    amount = Decimal(request.data.get("amount"))

    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user_id=user_id)

        wallet.balance = F('balance') + amount
        wallet.save()

        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            type=Transaction.CREDIT
        )

    return Response({"message": "Wallet credited successfully"})

@api_view(['POST'])
@permission_classes([IsAdminUserCustom])
def debit_wallet(request):
    user_id = request.data.get("user_id")
    amount = Decimal(request.data.get("amount"))

    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user_id=user_id)

        if wallet.balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        wallet.balance = F('balance') - amount
        wallet.save()

        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            type=Transaction.DEBIT
        )

    return Response({"message": "Wallet debited successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_balance(request):
    wallet = Wallet.objects.get(user=request.user)
    return Response({"balance": wallet.balance})