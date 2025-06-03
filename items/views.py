import logging

import stripe
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item
from .serializers import ItemSerializer

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'item.html'

    def get(self, request: Request, item_id: int) -> Response:
        try:
            item = Item.objects.get(id=item_id, price__gte=settings.MIN_ITEM_PRICE)
            serializer = ItemSerializer(item)
            return Response({'item': serializer.data})
        except Item.DoesNotExist:
            return Response(
                {'error': f'Item with id {item_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class BuyAPIView(APIView):
    def get(self, request: Request, item_id: int) -> Response:
        try:
            item = Item.objects.get(id=item_id, price__gte=settings.MIN_ITEM_PRICE)

            cancel_url = request.build_absolute_uri(
                reverse('item',
                        kwargs={'item_id': item.id}  # type:ignore
                        )
            )

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': item.currency,
                            'product_data': {
                                'name': item.name,
                                'description': item.description,
                            },
                            'unit_amount': int(item.price * 100),
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=settings.STRIPE_SUCCESS_URL,
                cancel_url=cancel_url,
            )
            return Response({'sessionId': session.id})
        except Item.DoesNotExist:
            return Response(
                {'error': f'Item with id {item_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
