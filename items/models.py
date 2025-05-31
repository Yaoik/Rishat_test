from django.core.validators import MinValueValidator
from django.db import models

from common.models import Timestamped


class Item(Timestamped):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Цена не может быть отрицательной или равной нулю"
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> str:
        return f'Товар \"{self.name}\"'
