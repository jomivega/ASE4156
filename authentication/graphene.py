from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphene import AbstractType


class GUser(DjangoObjectType):
    class Meta:
        model = User


class Query(AbstractType):
    pass
