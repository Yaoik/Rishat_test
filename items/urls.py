from django.urls import path

from .views import BuyAPIView, ItemHTMLView

urlpatterns = [
    path('item/<int:item_id>/', ItemHTMLView.as_view(), name='item'),
    path('buy/<int:item_id>/', BuyAPIView.as_view(), name='buy-item'),
]
