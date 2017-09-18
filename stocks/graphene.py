from graphene_django import DjangoObjectType
from .models import DailyStockQuote, Stock
from graphene import AbstractType, relay


class GStock(DjangoObjectType):
    class Meta:
        model = Stock
        interfaces = (relay.Node, )


class GDailyStockQuote(DjangoObjectType):
    class Meta:
        model = DailyStockQuote
        interfaces = (relay.Node, )


class Query(AbstractType):
    pass
