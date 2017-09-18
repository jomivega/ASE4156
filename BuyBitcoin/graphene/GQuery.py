import graphene
from .GUser import GUser


class GQuery(graphene.ObjectType):
    viewer = graphene.Field(GUser, )

    def resolve_viewer(self, args, context, info):
        return context.user
