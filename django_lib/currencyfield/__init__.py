from fields import CurrencyField

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^currencyfield\.fields\.CurrencyField"])
except ImportError:
    pass
