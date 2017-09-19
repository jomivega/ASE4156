"""
The overarching GraphQL schema. Here is where all queries come together
to form one schema
"""
import graphene

import stocks.graphene
import trading.graphene
import authentication.graphene


# pylint: disable=too-few-public-methods
class Query(
        authentication.graphene.Query,
        stocks.graphene.Query,
        trading.graphene.Query,
        graphene.ObjectType):
    """
    Combination of all queries of all apps
    """
    pass
# pylint: enable=too-few-public-methods


SCHEMA = graphene.Schema(query=Query)