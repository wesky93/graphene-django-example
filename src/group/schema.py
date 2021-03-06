import graphene
from graphene_django.types import DjangoObjectType

from .models import Organizer, UserGroup


# default GraphQL
class UserGroupType(DjangoObjectType):
    class Meta:
        model = UserGroup


class OrganizerType(DjangoObjectType):
    class Meta:
        model = Organizer
        fields = ('name','slack_id','user')


# GraphQL Relay
class UserGroupNode(DjangoObjectType):
    class Meta:
        model = UserGroup
        interfaces = (graphene.relay.Node,)


class UserGroupConnection(graphene.relay.Connection):
    class Meta:
        node = UserGroupNode


class OrganizerNode(DjangoObjectType):
    class Meta:
        model = Organizer
        interfaces = (graphene.relay.Node,)


class OrganizerConnection(graphene.relay.Connection):
    class Meta:
        node = OrganizerNode


class Query(object):
    # default GraphQL
    user_group_type = graphene.Field(UserGroupType)
    organizer_type = graphene.Field(OrganizerType)
    all_user_groups = graphene.List(UserGroupType)
    all_organizers = graphene.List(OrganizerType)

    def resolve_all_user_groups(self, info, **kwargs):
        return UserGroup.objects.all()

    def resolve_all_organizers(self, info, **kwargs):
        return Organizer.objects.all()

    # GraphQL Relay
    user_group = graphene.relay.Node.Field(UserGroupNode)
    user_groups = graphene.relay.ConnectionField(UserGroupConnection)
    organizer = graphene.relay.Node.Field(OrganizerNode)
    organizers = graphene.relay.ConnectionField(OrganizerConnection)

    def resolve_user_groups(self, info, **kwargs):
        return UserGroup.objects.all()

    def resolve_organizers(self, info, **kwargs):
        return Organizer.objects.all()
