from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from common.models import Timestamped

from .choices import CurrencyChoices


class Item(Timestamped):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(settings.MIN_ITEM_PRICE)],
        help_text="Цена не может быть отрицательной или равной нулю"
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices,
        default='usd'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return f'Товар \"{self.name}\"'
