from decimal import Decimal, getcontext

from django.conf import settings
from django.core.cache import cache
from forex_python.converter import CurrencyRates, RatesNotAvailableError

getcontext().prec = 8


def get_cached_conversion(from_currency: str, to_currency: str, amount: Decimal) -> Decimal:
    """Функция для получения курса валют"""
    from_currency, to_currency = from_currency.upper(), to_currency.upper()
    if from_currency == to_currency:
        return amount

    cache_key = f"currency_rate_{from_currency}_{to_currency}"
    rate = cache.get(cache_key)

    if rate is None:
        try:
            c = CurrencyRates(force_decimal=True)
            rate = Decimal(str(c.get_rate(from_currency, to_currency)))
            cache.set(cache_key, float(rate), timeout=settings.CURRENCY_CONVERSION_CACHE_TIMEOUT)
        except RatesNotAvailableError:
            rate = Decimal('1')

    return amount * Decimal(str(rate))
