from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    CartSerializer, CartItemSerializer,
    OrderSerializer, OrderStatusUpdateSerializer
)
from shop.models import Product


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=CartSerializer)
    def list(self, request):
        cart, _ = Cart.objects.prefetch_related(
            'items__product__category'
        ).get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @extend_schema(request=CartItemSerializer, responses=CartSerializer)
    def create(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(
            Product,
            id=serializer.validated_data['product_id'],
            is_active=True
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': serializer.validated_data['quantity']}
        )

        if not created:
            cart_item.quantity += serializer.validated_data['quantity']
            cart_item.save()

        cart.refresh_from_db()
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    @extend_schema(request=CartItemSerializer, responses=CartItemSerializer)
    def partial_update(self, request, pk=None):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, id=pk, cart=cart)
        quantity = request.data.get('quantity')

        if not quantity or int(quantity) < 1:
            return Response(
                {'error': 'Количество должно быть не менее 1.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.quantity = int(quantity)
        item.save()
        return Response(CartItemSerializer(item).data)

    @extend_schema(responses={204: None})
    def destroy(self, request, pk=None):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, id=pk, cart=cart)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=OrderSerializer)
    def list(self, request):
        orders = Order.objects.filter(
            user=request.user
        ).prefetch_related('items__product').order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @extend_schema(request=None, responses=OrderSerializer)
    def create(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        items = cart.items.select_related('product').all()

        if not items.exists():
            return Response(
                {'error': 'Корзина пуста.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        total = sum(item.subtotal for item in items)

        order = Order.objects.create(
            user=request.user,
            total_price=total,
            status=Order.STATUS_NEW
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.items.all().delete()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

    @extend_schema(responses=OrderSerializer)
    def retrieve(self, request, pk=None):
        order = get_object_or_404(
            Order,
            id=pk,
            user=request.user
        )
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @extend_schema(request=OrderStatusUpdateSerializer, responses=OrderSerializer)
    def partial_update(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {'error': 'Нет прав.'},
                status=status.HTTP_403_FORBIDDEN
            )
        order = get_object_or_404(Order, id=pk)
        serializer = OrderStatusUpdateSerializer(
            order, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(order).data)