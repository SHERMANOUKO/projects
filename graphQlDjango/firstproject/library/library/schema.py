import graphene
import graphql_jwt
import books.schema

class Query(
    books.schema.RelayQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    books.schema.Mutations,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)