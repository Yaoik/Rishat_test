from django.urls import path

from .views import BuyOrderAPIView, OrderHTMLView

urlpatterns = [
    path('order/<int:order_id>/', OrderHTMLView.as_view(), name='order'),
    path('buy-order/<int:order_id>/', BuyOrderAPIView.as_view(), name='buy-order'),
]
