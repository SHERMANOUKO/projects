import os
import boto3
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework import status
from adminportal.serializers import CaretakerSerializer, CaretakerSerializerNoPhoto, \
    CaretakerSerializerPhoto, ReadCaretakerSerializer
from adminportal.models import Caretakers, CustomUser
from adminportal.services.filename import randomString

class CaretakerController():
    """handles caretaker requests"""
    def _unknown_exception(self, exception):
        """Returns an unanticipated exception"""
        return Response(
            {'details':str(exception), 'code': 500},
            status=status.HTTP_200_OK
        )

    def create_caretaker(self, request):
        """create a caretaker"""
        serializer = CaretakerSerializer(data=request.data)
        if not serializer.is_valid():
            if 'username' in serializer.errors:
                try:
                    CustomUser.objects.get(username=serializer.initial_data['username'])
                except CustomUser.DoesNotExist:
                    return Response(
                        {'details':'The username provided does not exist', 'code': 400},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except KeyError:
                    return Response(
                        {'details':'No username provided', 'code': 400},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except Exception as exception:
                    return self._unknown_exception(exception)

            return Response(
                {'details':serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        try:
            Caretakers.objects.get(
                caretakerPhoneNumber=serializer.validated_data['caretakerPhoneNumber']
            )
            return Response(
                {'details':'Phone number Already Exists', 'code':400},
                status=status.HTTP_200_OK
            )
        except (Caretakers.DoesNotExist, KeyError):
            try:
                Caretakers.objects.get(
                    caretakerNationalID=serializer.validated_data['caretakerNationalID']
                )
                return Response(
                    {'details':'National ID number Already Exists', 'code':400},
                    status=status.HTTP_200_OK
                )
            except Caretakers.DoesNotExist:
                serializer.save()
                return Response(
                    {'details':'Caretaker succesfully added', 'code':200},
                        status=status.HTTP_200_OK
                    )
            except Exception as exception:
                return self._unknown_exception(exception)
        except Exception as exception:
            return self._unknown_exception(exception)

    def list_caretakers(self, request):
        """lists all caretakers"""
        try:
            queryset = Caretakers.objects.all()
            serializer = ReadCaretakerSerializer(queryset, many=True)
            if not serializer.data:
                return Response(
                    {'details':'No caretakers added to database yet.', 'code':400},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)
        
    def update_caretaker(self, request, caretaker_id):
        """update a caretaker"""
        try:
            serializer = CaretakerSerializerNoPhoto(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'details':serializer.errors, 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            caretaker = Caretakers.objects.filter(caretakerID=caretaker_id)
            
            if caretaker:
                caretaker.update(**serializer.data)
                return Response(
                    {'details':'Caretaker succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':'Caretaker to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            if type(exception).__name__ == 'IntegrityError':
                return Response(
                    {
                        'details':'Another caretaker already has '\
                                    'the ID number or phone number you are trying to use',
                        'code':400
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':str(exception), 'code':500}
            )

    def delete_caretaker(self, caretaker_id):
        """deletes a caretaker"""
        try:
            caretaker = Caretakers.objects.get(caretakerID=caretaker_id)
            self.bucket_name = 'krypto-files'
            self.object_name = 'media/profile/caretakers/'+str(caretaker.caretakerAvatar)

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
            Caretakers.objects.filter(caretakerID=caretaker_id).delete()
            return Response(
                {'details':'Succesfully deleted caretaker.', 'code':200},
                status=status.HTTP_200_OK
            )
        except:
            Caretakers.objects.filter(caretakerID=caretaker_id).delete()
            return Response(
                {'details':'Succesfully deleted caretaker.', 'code':200},
                status=status.HTTP_200_OK
            )

    def get_avatar(self, request, caretaker_id):
        """get one photo"""
        try:
            caretaker = Caretakers.objects.get(caretakerID=caretaker_id)
            filename = randomString() + str(caretaker.caretakerAvatar)
            
            self.s3 = boto3.client(
                's3',
                aws_access_key_id='AKIAVJ3LWIU3CRDMYUPF',
                aws_secret_access_key='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',
            )

            self.bucket_name = 'krypto-files'
            self.object_name = 'media/profile/caretakers/'+str(caretaker.caretakerAvatar)

            with open(filename, 'wb') as caretaker_avatar:
                self.s3.download_fileobj(self.bucket_name, self.object_name, caretaker_avatar)
            
            file = open(filename, 'rb')
            os.remove(filename)
            return FileResponse(file)
        except Exception:
            # raise
            # if type(e).__name__ == 'ClientError':
            return Response()

    def update_avatar(self, request):
        """update caretaker avatar"""
        try:
            serializer = CaretakerSerializerPhoto(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'details':serializer.errors, 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )

            caretaker = Caretakers.objects.get(caretakerNationalID=serializer.validated_data['caretakerNationalID'])
            
            if caretaker:
                caretaker.caretakerAvatar = request.FILES['caretakerAvatar']
                caretaker.save()
                return Response(
                    {'details':'Caretaker succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':'Caretaker to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )
        except Caretakers.DoesNotExist:
            return Response(
                {'details': 'Caretaker with national ID provided does not exist', 'code': 400},
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

    def retrieve_caretaker(self, caretaker_id):
        """retrieve a single caretaker"""
        try:
            queryset = Caretakers.objects.get(caretakerID=caretaker_id)
            serializer = ReadCaretakerSerializer(queryset)
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Caretakers.DoesNotExist:
            return Response(
                {'details':'Caretaker Does Not Exist', 'code': 400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)

    