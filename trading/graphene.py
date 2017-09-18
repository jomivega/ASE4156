from graphene_django import DjangoObjectType
from .models import Trade
from .models import TradingAccount
from graphene import AbstractType


class GTrade(DjangoObjectType):
    class Meta:
        model = Trade


class GTradingAccount(DjangoObjectType):
    class Meta:
        model = TradingAccount


class Query(AbstractType):
    pass
