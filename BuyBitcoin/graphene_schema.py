import graphene

import stocks.graphene
import trading.graphene
import authentication.graphene


class Query(
        authentication.graphene.Query,
        stocks.graphene.Query,
        trading.graphene.Query,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
