from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'display_items')
    list_filter = ('created_at', 'updated_at')
    filter_horizontal = ('items',)
    readonly_fields = ('created_at', 'updated_at')

    def display_items(self, obj):
        return ", ".join([item.name for item in obj.items.all()])
    display_items.short_description = 'Товары'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items')
