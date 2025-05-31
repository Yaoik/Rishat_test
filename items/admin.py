from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'price')
    search_fields = ('name', 'description')
    list_editable = ('price',)
    ordering = ('name',)
    fields = ('name', 'description', 'price')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

    class Meta:
        model = Item
