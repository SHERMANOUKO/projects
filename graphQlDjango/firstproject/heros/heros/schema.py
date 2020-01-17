import graphene
import graphql_jwt
import hero.schema
import users.schema
import hero.schema_relay

class Query(users.schema.Query, hero.schema.Query, hero.schema_relay.RelayQuery, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, hero.schema.Mutation, hero.schema_relay.RelayMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)