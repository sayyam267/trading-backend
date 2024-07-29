from ..models import Order

class OrderService:
    @staticmethod
    def save_order(user, order_type, order_action, quantity, price, status, platform_type,symbol):
        order = Order.objects.create(
            user=user,
            order_type=order_type,
            order_action=order_action,
            quantity=quantity,
            price=price,
            status=status,
            platform_type=platform_type,
            symbol=symbol
        )
        try:
            order.save()
            return True
        except Exception as e:
            print('Error save order')
            return False

    @staticmethod
    def update_order_status(order_id, new_status):
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            return order
        except Order.DoesNotExist:
            return None
