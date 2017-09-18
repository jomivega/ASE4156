from graphene_django import DjangoObjectType
from .models import Trade
from .models import TradingAccount
from graphene import AbstractType, relay


class GTrade(DjangoObjectType):
    class Meta:
        model = Trade
        interfaces = (relay.Node, )


class GTradingAccount(DjangoObjectType):
    class Meta:
        model = TradingAccount
        interfaces = (relay.Node, )


class Query(AbstractType):
    pass
