from rest_framework import serializers

from items.serializers import ItemSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'items', ]
        read_only_fields = fields
