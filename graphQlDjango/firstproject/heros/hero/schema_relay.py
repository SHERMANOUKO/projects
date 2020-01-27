import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Hero

#1
class HeroFilter(django_filters.FilterSet):
    class Meta:
        model = Hero
        fields = ['name', 'movie']

#2
class HeroNode(DjangoObjectType):
    class Meta:
        model = Hero
        #3
        interfaces = (graphene.relay.Node, )

class RelayQuery(graphene.ObjectType):
    #4
    relay_hero = graphene.relay.Node.Field(HeroNode)
    #5
    relay_heros = DjangoFilterConnectionField(HeroNode, filterset_class=HeroFilter)

class RelayCreateHero(graphene.relay.ClientIDMutation):
    hero = graphene.Field(HeroNode)

    class Input:
        id = graphene.String()
        name = graphene.String()
        movie = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        hero = Hero(
            id=input.get('id'),
            name=input.get('name'),
            movie=input.get('movie')
        )
        hero.save()

        return 'saved'


class RelayMutation(graphene.AbstractType):
    relay_create_hero = RelayCreateHero.Field()