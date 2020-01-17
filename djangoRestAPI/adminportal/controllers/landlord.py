import os
import boto3
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework import status
from adminportal.serializers import LandlordSerializer, LandlordsSerializerNoPhoto, LandlordSerializerPhoto
from adminportal.models import Landlords, CustomUser
from adminportal.services.filename import randomString

class LandlordController():
    """handles landlord requests"""
    def _unknown_exception(self, exception):
        """Returns an unanticipated exception"""
        return Response(
            {'details':str(exception), 'code': 500},
            status=status.HTTP_200_OK
        )

    def create_landlord(self, request):
        """create a landlord"""
        serializer = LandlordSerializer(data=request.data)
        if not serializer.is_valid():
            if 'username' in serializer.errors:
                try:
                    CustomUser.objects.get(username=serializer.initial_data['username'])
                except CustomUser.DoesNotExist:
                    return Response(
                        {'details':'The username provided does not exist', 'code': 400},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(
                {'details':serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            Landlords.objects.get(
                landlordEmailAddress=serializer.validated_data['landlordEmailAddress']
            )
            return Response(
                {'details':'Email address Already Exists', 'code':400},
                status=status.HTTP_200_OK
            )
        except (Landlords.DoesNotExist, KeyError):
            try:
                Landlords.objects.get(
                    username=serializer.validated_data['username']
                )
                return Response(
                    {'details':'A landlord is already registered with that username', 'code':400},
                    status=status.HTTP_200_OK
                )
            except Landlords.DoesNotExist:
                try:
                    Landlords.objects.get(
                        landlordPrimaryPhoneNumber=serializer.validated_data['landlordPrimaryPhoneNumber']
                    )
                    return Response(
                        {'details':'Primary phone number Already Exists', 'code':400},
                        status=status.HTTP_200_OK
                    )
                except (Landlords.DoesNotExist, KeyError):
                    try:
                        Landlords.objects.get(
                            landlordSecondaryPhoneNumber=serializer.validated_data['landlordSecondaryPhoneNumber']
                        )
                        return Response(
                            {'details':'Secondary phone number Already Exists', 'code':400},
                            status=status.HTTP_200_OK
                        )
                    except (Landlords.DoesNotExist, KeyError):
                        try:
                            Landlords.objects.get(
                                landlordNationalID=serializer.validated_data['landlordNationalID']
                            )
                            return Response(
                                {'details':'National ID number Already Exists', 'code':400},
                                status=status.HTTP_200_OK
                            )
                        except Landlords.DoesNotExist:
                            serializer.save()
                            return Response(
                                {'details':'Landlord succesfully added', 'code':200},
                                    status=status.HTTP_200_OK
                                )
                        except Exception as exception:
                            return self._unknown_exception(exception)
                    except Exception as exception:
                        return self._unknown_exception(exception)
                except Exception as exception:
                    return self._unknown_exception(exception)
            except Exception as exception:
                return self._unknown_exception(exception)
        except Exception as exception:
            return self._unknown_exception(exception)

    def list_landlords(self, request):
        """lists all landlords"""
        try:
            queryset = Landlords.objects.all()
            serializer = LandlordSerializer(queryset, many=True)
            if not serializer.data:
                return Response(
                    {'details':'No landlords added to database yet.', 'code':400},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)
        
    def update_landlord(self, request, landlord_id):
        """update a landlord"""
        try:
            serializer = LandlordsSerializerNoPhoto(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'details':serializer.errors, 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            landlord = Landlords.objects.filter(landlordID=landlord_id)
            
            if landlord:
                landlord.update(**serializer.data)
                return Response(
                    {'details':'Landlord succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':'Landlord to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            if type(exception).__name__ == 'IntegrityError':
                return Response(
                    {
                        'details':'Another region already has '\
                                    'the eamil, ID number or phone number you are trying to use',
                        'code':400
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':str(exception), 'code':500}
            )

    def delete_landlord(self, landlord_id):
        """deletes a landlord"""
        try:
            landlord = Landlords.objects.get(landlordID=landlord_id)
            self.bucket_name = 'krypto-files'
            self.object_name = 'media/profile/landlords/'+str(landlord.landlordAvatar)

            # self.object_name = self.object_name+agent.agentAvatar
            self.s3 = boto3.client(
                's3',
                aws_access_key_id='AKIAVJ3LWIU3CRDMYUPF',
                aws_secret_access_key='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',
            )

            self.s3.delete_object(
                Bucket=self.bucket_name,
                Key=self.object_name,
            )
            Landlords.objects.filter(landlordID=landlord_id).delete()
            return Response(
                {'details':'Succesfully deleted Landlord.', 'code':200},
                status=status.HTTP_200_OK
            )
        except:
            Landlords.objects.filter(landlordID=landlord_id).delete()
            return Response(
                {'details':'Succesfully deleted landlord.', 'code':200},
                status=status.HTTP_200_OK
            )

    def get_avatar(self, request, landlord_id):
        """get one photo"""
        try:
            landlord = Landlords.objects.get(landlordID=landlord_id)
            filename = randomString() + str(landlord.landlordAvatar)
            
            self.s3 = boto3.client(
                's3',
                aws_access_key_id='AKIAVJ3LWIU3CRDMYUPF',
                aws_secret_access_key='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',
            )

            self.bucket_name = 'krypto-files'
            self.object_name = 'media/profile/landlords/'+str(landlord.landlordAvatar)

            with open(filename, 'wb') as landlord_avatar:
                self.s3.download_fileobj(self.bucket_name, self.object_name, landlord_avatar)
            
            file = open(filename, 'rb')
            os.remove(filename)
            return FileResponse(file)
        except Exception:
            # raise
            # if type(e).__name__ == 'ClientError':
            return Response()

    def update_avatar(self, request):
        try:
            serializer = LandlordSerializerPhoto(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'details':serializer.errors, 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )

            landlord = Landlords.objects.get(landlordNationalID=serializer.validated_data['landlordNationalID'])
            
            if landlord:
                landlord.landlordAvatar = request.FILES['landlordAvatar']
                landlord.save()
                return Response(
                    {'details':'Landlord succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':'Landlord to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            # raise
            if type(exception).__name__ == 'IntegrityError':
                return Response(
                    {
                        'details': str(exception),
                        'code':400
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':str(exception), 'code':500}
            )

    def retrieve_landlord(self, landlord_id):
        """retrieve a single landlord"""
        try:
            queryset = Landlords.objects.get(landlordID=landlord_id)
            serializer = LandlordSerializer(queryset)
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Landlords.DoesNotExist:
            return Response(
                {'details':'Landlord Does Not Exist', 'code': 400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)

    