from django.urls import path

from orders.views import CreateOrderView, DetailOrderView, UpdateOrderStatusView

urlpatterns = [
    path('orders/create/', CreateOrderView.as_view(), name='place_order'),
    path('orders/<int:order_id>/', DetailOrderView.as_view(), name='view_order'),
    path('orders/<int:order_id>/update_status/', UpdateOrderStatusView.as_view(), name='update_order_status'),
]