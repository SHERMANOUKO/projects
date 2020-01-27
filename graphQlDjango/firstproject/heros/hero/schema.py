import graphene
from graphene_django import DjangoObjectType

from .models import Hero
from django.db.models import Q

class HeroType(DjangoObjectType):
    class Meta:
        model = Hero

class Query(graphene.ObjectType):
    heroes = graphene.List(HeroType,name=graphene.String())
    singleHero = graphene.List(HeroType,
                              id=graphene.String(),
                              name=graphene.String(),
                              movie=graphene.String())

    def resolve_heroes(self, info, **kwargs):
        if kwargs.get('name') is not None:
            filter = (
                Q(name=kwargs.get('name'))
            )
            return Hero.objects.filter(filter)
            
        return Hero.objects.all()

    def resolve_singleHero(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        movie = kwargs.get('movie')

        if movie is not None:
            return Hero.objects.get(movie=movie)

        if id is not None:
            return Hero.objects.get(id=id)

        if name is not None:
            return Hero.objects.filter(name=name)

        return None

class CreateHero(graphene.Mutation):
    id = graphene.String()
    name = graphene.String()
    movie = graphene.String()

    class Arguments:
        id = graphene.String()
        name = graphene.String()
        movie = graphene.String()

    def mutate(self, info, id, name, movie):
        heroes = Hero(id=id, name=name, movie=movie)
        heroes.save()

        return CreateHero(
            id=heroes.id,
            name=heroes.name,
            movie=heroes.movie,
        )

class Mutation(graphene.ObjectType):
    createHero = CreateHero.Field()