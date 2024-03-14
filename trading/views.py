from django.shortcuts import render
from .services.binance import BinanceService

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import json
from .models import Credential
from .serializers import CredentialCreateSerializer,CredentialRetrieveSerializer

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

    import pdb

    pdb.set_trace()

    p_record = get_object_or_404(Credential, unique_token=uuid)
    if p_record:
        if p_record.platform_type == 'binance':
            binance_srv = BinanceService(p_record.api_key,p_record.secret_key)
            binance_srv.create_test_order(data.get('side'),data.get('quantity'),data.get('symbol'),data.get('type'))
    
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
    response_data = {'status': 'success', 'message': 'Order received successfully'}
    return Response(response_data)

