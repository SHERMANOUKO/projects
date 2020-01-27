import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Category, Books
from graphql import GraphQLError

class BooksFilter(django_filters.FilterSet):
    class Meta:
        model = Books
        fields = ['bookName','category','bookAuthor']

class BooksNode(DjangoObjectType):
    class Meta:
        model = Books
        interfaces = (graphene.relay.Node, )

class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'categoryName':['iexact','exact','icontains','istartswith']
        }

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (graphene.relay.Node, )

    message = graphene.String()
    code = graphene.Int()

class RelayQuery(graphene.ObjectType):
    relay_book = graphene.relay.Node.Field(BooksNode)
    relay_books = DjangoFilterConnectionField(BooksNode, filterset_class=BooksFilter, bookID=graphene.String(required=True))
    relay_category = graphene.Field(CategoryNode,categoryID=graphene.Int(required=True))
    relay_categories = DjangoFilterConnectionField(CategoryNode, filterset_class=CategoryFilter)
    

    def resolve_relay_category(self, info, **kwargs):
        categoryID = kwargs.get('categoryID')
        try:
            return CategoryNode(categoryName=Category.objects.get(pk=categoryID).categoryName ,code=200,message="Category Found")
        except Exception as e:
            if type(e).__name__ == 'DoesNotExist':
                return CategoryNode(code=401, message="Category Does Not Exist", categoryName="")
            else:
                return CategoryNode(code=401, message=str(e), categoryName="")

    def resolve_relay_book(self, info, **kwargs):
        bookID = kwargs.get('bookID')
        try:
            return BooksNode(bookName=Category.objects.get(pk=bookID).bookName ,code=200,message="Book Found")
        except Exception as e:
            if type(e).__name__ == 'DoesNotExist':
                return BooksNode(code=401, message="Book Does Not Exist", bookName="")
            else:
                return BooksNode(code=401, message=str(e), bookName="")
        

class CreateBook(graphene.relay.ClientIDMutation):
    class Input:
        bookID = graphene.String(required=True)
        bookName = graphene.String(required=True)
        bookAuthor = graphene.String(required=True)
        category = graphene.Int(required=True)

    created = graphene.Boolean()
    message = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        addedBook = Books(
            bookID = input.get('bookID'),
            bookName = input.get('bookName'),
            bookAuthor = input.get('bookAuthor'),
            category = input.get('category')
        )
        try:
            addedBook.save()
            created = True
            message = "succesfully created book"
        except Exception as e:
            created = False
            message = str(e)
        return CreateBook(created=created, message=message)

class CreateCategory(graphene.relay.ClientIDMutation):
    class Input:
        categoryName = graphene.String(required=True)

    created = graphene.Boolean()
    message = graphene.String()

    def mutate_and_get_payload(root,info,**input):
        addedCategory = Category(
            categoryName = input.get('categoryName')
        )

        try:
            addedCategory.save()
            created = True
            message = "succesfully created category"
        except Exception as e:
            created = False
            message = str(e)
        return CreateCategory(created=created,message=message)

class UpdateCategory(graphene.relay.ClientIDMutation):
    class Input:
        categoryName = graphene.String(required=True)
        categoryID = graphene.Int(required=True)

    code = graphene.Int()
    message = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        categoryName = input.get('categoryName')
        categoryID = input.get('categoryID')

        try:
            categoryObject = Category.objects.get(pk=categoryID)
            if categoryObject:
                if Category.objects.get(categoryName=categoryName):
                    return CategoryNode(categoryName=categoryName,categoryID=categoryID,code=200,message="Category Name Already Exists")

                categoryObject.categoryName = categoryName
                categoryObject.save()
                return CategoryNode(categoryName=categoryName,categoryID=categoryID,code=200,message="Category Updated")
        except Exception as e:
            if type(e).__name__ == 'DoesNotExist':
                return CategoryNode(code=401, message="Category Does Not Exist", categoryName=categoryName,categoryID=categoryID)
            return CategoryNode(code=401, message=str(e), categoryName=categoryName,categoryID=categoryID)

class UpdateBook(graphene.relay.ClientIDMutation):
    class Input:
        bookName = graphene.String(required=True)
        bookID = graphene.String(required=True)

    code = graphene.Int()
    message = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        bookName = input.get('bookName')
        bookID = input.get('bookID')

        try:
            bookObject = Books.objects.get(pk=bookID)
            if bookObject:
                bookObject.bookName = bookName
                bookObject.save()
                return BooksNode(bookName=bookName,bookID=bookID,code=200,message="Book Updated")
        except Exception as e:
            if type(e).__name__ == 'DoesNotExist':
                return BooksNode(code=401, message="Book Does Not Exist", bookName=bookName,bookID=bookID)
            return BooksNode(code=401, message=str(e), bookName=bookName,bookID=bookID)


class DeleteBook(graphene.relay.ClientIDMutation):
    class Input:
        bookID = graphene.String(required=True)

    code = graphene.Int()
    message = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        bookID = input.get('bookID')

        try:
            bookObject = Books.objects.get(pk=bookID)
            if bookObject:
                bookObject.delete()
                return BooksNode(bookID=bookID,code=200,message="Book Deleted")
        except Exception as e:
            if type(e).__name__ == 'DoesNotExist':
                return BooksNode(code=401, message="Book Does Not Exist", bookID=bookID)
            return BooksNode(code=401, message=str(e), bookID=bookID)

class DeleteCategory(graphene.relay.ClientIDMutation):
    class Input:
        categoryID = graphene.Int(required=True)

    code = graphene.Int()
    message = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        categoryID = input.get('categoryID')

        try:
            categoryObject = Category.objects.get(pk=categoryID)
            if categoryObject:
                categoryObject.delete()
                return CategoryNode(categoryID=categoryID,code=200,message="Category Deleted")
        except Exception as e:
            if type(e).__name__ == 'DoesNotExist':
                return CategoryNode(code=401, message="Category Does Not Exist", categoryID=categoryID)
            return CategoryNode(code=401, message=str(e), categoryID=categoryID)

class Mutations(graphene.AbstractType):
    create_book = CreateBook.Field()
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
    delete_category = DeleteCategory.Field()