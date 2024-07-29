from django.urls import path
from .views import CredentialCreateView,webhook_view,UserOrderListView,order_count_by_type

urlpatterns = [
    path("platform", CredentialCreateView.as_view(), name="add_binance_creds"),
    path('webhook/<uuid:uuid>', webhook_view, name='webhook'),
    path('orders', UserOrderListView.as_view(), name='user_order_list'),
    path('orders-count', order_count_by_type, name='user_order_count'),
]