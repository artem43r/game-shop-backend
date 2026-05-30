from django.urls import path
from . import views

cart_list = views.CartViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

cart_detail = views.CartViewSet.as_view({
    'patch': 'partial_update',
    'delete': 'destroy',
})

order_list = views.OrderViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

order_detail = views.OrderViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

urlpatterns = [
    path('cart/', cart_list, name='cart'),
    path('cart/items/<int:pk>/', cart_detail, name='cart-item-detail'),
    path('orders/', order_list, name='order-list'),
    path('orders/<int:pk>/', order_detail, name='order-detail'),
]