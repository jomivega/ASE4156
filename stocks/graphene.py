from graphene_django import DjangoObjectType
from .models import DailyStockQuote, Stock
from graphene_django import DjangoObjectType
from graphene import AbstractType, List


class GStock(DjangoObjectType):
    class Meta:
        model = Stock


class GDailyStockQuote(DjangoObjectType):
    class Meta:
        model = DailyStockQuote


class Query(AbstractType):
    all_stocks = List(GStock)

    def resolve_all_stocks(self, info, **kwargs):
        return Stock.objects.all()
