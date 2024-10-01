from .models import Order


def update_order_status(order_id, new_status):
    print("Updating the order status.")
    order = Order.objects.get(id=order_id)
    
    if order:
        order.order_status = new_status
        order.save()
        
        return "Order status updated."
    else:
        return "Order doesnot exist."