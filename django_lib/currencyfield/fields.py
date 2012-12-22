from django.db import models
from decimal import Decimal

class CurrencyField(models.DecimalField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, verbose_name=None, name=None, **kwargs):
        super(CurrencyField, self). __init__(
            verbose_name=verbose_name, name=name, max_digits=7,
            decimal_places=2, **kwargs)

    def to_python(self, value):
        try:
           return super(CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
        except AttributeError:
           return None
