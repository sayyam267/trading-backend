from django.shortcuts import render
from .services.binance import BinanceService

from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import json
from .models import Credential,Order
from .serializers import CredentialCreateSerializer,CredentialRetrieveSerializer,OrderSerializer
from .services.order import OrderService

from django.shortcuts import get_object_or_404

class CredentialCreateView(generics.ListCreateAPIView):
    queryset = Credential.objects.all()
    # serializer_class = CredentialSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CredentialCreateSerializer
        return CredentialRetrieveSerializer

    def get_queryset(self):
        user = self.request.user
        return Credential.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([AllowAny])
def webhook_view(request, uuid):
    # Extract data from the request
    data = json.loads(request.body.decode('utf-8'))

    # import pdb

    # pdb.set_trace()

    p_record = get_object_or_404(Credential, unique_token=uuid)
    if p_record:
        if p_record.platform_type == 'binance' or p_record.platform_type == 'oanda' or p_record.platform_type == 'alpaca':
            binance_srv = BinanceService(p_record.api_key,p_record.secret_key)
            trades = binance_srv.create_test_order(data.get('side'),data.get('quantity'),data.get('symbol'),data.get('type'))
            # trades = binance_srv.create_order(data.get('side'),data.get('quantity'),data.get('symbol'),data.get('type'))
            print(trades)
            order_srv = OrderService()
            order_srv.save_order(user=p_record.user,order_type='market',order_action=data.get('side'),quantity=data.get('quantity'),price=0.000027,status='filled',platform_type=p_record.platform_type,symbol=data.get('symbol'))
    
    # Process the order data (replace this with your actual order processing logic)
    symbol = data.get('symbol')
    side = data.get('side')
    quantity = data.get('quantity')
    o_type = data.get('type')
    # ... add more fields as needed

    # Perform order processing logic here (this is a placeholder)
    # Replace this with your actual order processing logic
    print(f"Order info-> Side: {side} | Quantity: {quantity} | Symbol: {symbol} | Type: {o_type}")

    # Respond to TradingView with a success message
    response_data = {'status': 'success', 'message': 'Order received successfully','data':trades}
    return Response(response_data)




class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer  # Replace with your serializer class
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can access this view

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
    

@api_view(['GET'])
def order_count_by_type(request):
    if request.user.is_authenticated:
        user = request.user

        # Get the count of orders for each type
        platform_types = ['binance', 'oanda', 'alpace']  # Define your order types
        order_count = {}
        for platform_type in platform_types:
            count = Order.objects.filter(user=user, platform_type=platform_type).count()
            order_count[platform_type.title()] = count

        return Response(order_count, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


