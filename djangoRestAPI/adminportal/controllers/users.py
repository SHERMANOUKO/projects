from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from adminportal.models import CustomUser
from adminportal.serializers import CustomUserSerializer, MinifiedUserSerializer

class UsersController():
    """handles users request"""
    def _unknown_exception(self, exception):
        """Returns an unanticipated exception"""
        return Response(
            {'details':str(exception), 'code': 500},
            status=status.HTTP_200_OK
        )

    def list_users(self, request):
        """list all users"""
        queryset = CustomUser.objects.all()
        serializer = MinifiedUserSerializer(queryset, many=True)

        if not serializer.data:
            return Response(
                {'details': 'No user added to databse', 'code': 400},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {'details': serializer.data, 'code': 200},
            status=status.HTTP_200_OK
        )

    def list_usertype_users(self, usertype):
        """list all agent users"""
        if not usertype:
            return Response(
                {'details': 'Invalid Usertype', 'code': 400},
                status=status.HTTP_200_OK
            )
            
        queryset = CustomUser.objects.all().filter(user_type=usertype)
        serializer = MinifiedUserSerializer(queryset, many=True)

        if not serializer.data:
            return Response(
                {'details': 'No user added to databse', 'code': 400},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {'details': serializer.data, 'code': 200},
            status=status.HTTP_200_OK
        )

    def create_user(self, request):
        """create a user"""
        serializer = CustomUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'details': serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            CustomUser.objects.get(username=serializer.validated_data['username'])
            return Response(
                {
                    'details':'The username already exists. Kindly select a different one',
                    'code': 400
                },
                status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            try:
                if serializer.validated_data.get('email'):
                    CustomUser.objects.get(email=serializer.validated_data['email'])
                    return Response(
                        {
                            'details':'The email already exists.',
                            'code': 400
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    serializer.validated_data['password']=make_password(serializer.validated_data['password'])
                    serializer.save()
                    return Response(
                        {'details':'Registration Succesful', 'code': 200},
                        status=status.HTTP_200_OK
                    )

            except CustomUser.DoesNotExist:
                serializer.save()
                return Response(
                    {'details':'Registration Succesful', 'code': 200},
                    status=status.HTTP_200_OK
                )
            except Exception as exception:
                return self._unknown_exception(exception)

        except Exception as exception:
            return self._unknown_exception(exception)

    def update_user(self, request, username):
        """update a region"""
        try:
            serializer = CustomUserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'details':serializer.errors, 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            user = CustomUser.objects.filter(username=username)
            
            if user:
                user.update(**serializer.data)
                return Response(
                    {'details':'User succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':'User to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            if type(exception).__name__ == 'IntegrityError':
                return Response(
                    {
                        'details':'Another User already has '\
                                    'the username you are trying to use',
                        'code':400
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':str(exception), 'code':500}
            )

    def delete_user(self, username):
        """delete a user"""
        user = CustomUser.objects.filter(username=username)
        if len(user) == 1 and user.is_superuser:
            return Response(
            {'details': 'Operation to delete this user is not allowed', 'code': 400},
                status=status.HTTP_200_OK
            )
        user.delete()
        return Response(
            {'details': 'User succesfully deleted', 'code': 200},
            status=status.HTTP_200_OK
        )

    def retrieve_user(self, username):
        """retrieve a single user"""
        try:
            queryset = CustomUser.objects.get(username=username)
            serializer = MinifiedUserSerializer(queryset)
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {'details':'User Does Not Exist', 'code': 400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)
            