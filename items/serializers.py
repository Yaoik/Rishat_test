from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'currency', ]
        read_only_fields = fields


class ItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', ]
        read_only_fields = ['name', 'description', 'price', ]
