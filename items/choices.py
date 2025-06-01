from django.db import models


class CurrencyChoices(models.TextChoices):
    RUB = "rub", "Рубли"
    USD = "usd", "Доллары"
