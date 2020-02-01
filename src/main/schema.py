import graphene

from group.schema import Query as groupQuery


class Query(graphene.ObjectType, groupQuery):
    pass


schema = graphene.Schema(query=Query)
