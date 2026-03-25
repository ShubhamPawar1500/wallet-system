from django.shortcuts import render
from decimal import Decimal

from django.db import transaction
from django.db.models import F

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order
from wallet.models import Transaction, Wallet

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    amount = Decimal(request.data.get("amount"))
    user = request.user

    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=user)

        if wallet.balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        wallet.balance = F('balance') - amount
        wallet.save()

        order = Order.objects.create(
            user=user,
            amount=amount
        )

        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            type=Transaction.DEBIT,
            reference=f"Order {order.id}"
        )

    return Response({"order_id": order.id})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    return Response({
        "id": order.id,
        "amount": order.amount,
        "status": order.status
    })