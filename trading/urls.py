from django.urls import path
from .views import CredentialCreateView,webhook_view

urlpatterns = [
    path("platform", CredentialCreateView.as_view(), name="add_binance_creds"),
    path('webhook/<uuid:uuid>', webhook_view, name='webhook'),
]