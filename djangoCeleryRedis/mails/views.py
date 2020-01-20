from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from mails.serializers import AccountsSerializer
from mails.models import Accounts

class CreateAccount(CreateAPIView):
    serializer_class = AccountsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Account created succesfuly',
            }
        
        return Response(response, status=status_code)

