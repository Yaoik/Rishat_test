from django.db import models

from common.models import Timestamped


class Order(Timestamped):
    items = models.ManyToManyField(
        "items.Item",
        related_name="orders",
        verbose_name="Товары в заказе",
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        return f"Заказ #{self.pk}"
