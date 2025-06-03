import logging
from decimal import Decimal, getcontext

import stripe
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils.currency_utils import get_cached_conversion
from items.choices import CurrencyChoices

from .models import Order
from .serializers import OrderSerializer

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'order.html'

    def get(self, request: Request, order_id: int) -> Response:
        try:
            order = Order.objects.get(id=order_id)
            currency = request.query_params.get('currency', 'usd').lower()
            valid_currencies = [choice[0] for choice in CurrencyChoices.choices]
            if currency not in valid_currencies:
                return Response(
                    {'error': f'Invalid currency. Available choices: {valid_currencies}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            total_price = 0
            order_data = OrderSerializer(order).data
            try:
                for item in order_data['items']:
                    if item['currency'].lower() != currency.lower():
                        item['price'] = get_cached_conversion(
                            item['currency'],
                            currency,
                            Decimal(item['price'])
                        )
                        item['currency'] = currency.lower()
                    total_price += Decimal(item['price'])
            except Exception as e:
                logger.error(f'{e=}')
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            logger.info(f'{order_data=}')
            return Response({'order': order_data, 'currency': currency, 'total_price': total_price})
        except Order.DoesNotExist:
            return Response(
                {'error': f'Order with id {order_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class BuyOrderAPIView(APIView):
    def get(self, request: Request, order_id: int) -> Response:
        try:
            currency = request.query_params.get('currency', 'usd')
            order = Order.objects.get(id=order_id)

            cancel_url = request.build_absolute_uri(
                reverse('order',
                        kwargs={'order_id': order.id}  # type:ignore
                        )
            )

            line_items = []
            for item in order.items.all():
                unit_amount = get_cached_conversion(item.currency, currency, item.price)

                line_items.append({
                    'price_data': {
                        'currency': currency,
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': int(unit_amount * 100),
                    },
                    'quantity': 1,
                })

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=settings.STRIPE_SUCCESS_URL,
                cancel_url=cancel_url,
            )

            return Response({'sessionId': session.id})
        except Order.DoesNotExist:
            return Response(
                {'error': f'Order with id {order_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
