import boto3
from rest_framework.response import Response
from rest_framework import status
from adminportal.serializers import ApartmentSerializer, ApartmentSerializerNoPhoto,\
    ApartmentSerializerPhoto, ReadApartmentSerializer
from adminportal.models import Apartments

class ApartmentController():
    """handles apartment requests"""
    def _unknown_exception(self, exception):
        """Returns an unanticipated exception"""
        return Response(
            {'details':str(exception), 'code': 500},
            status=status.HTTP_200_OK
        )

    def create_apartment(self, request):
        """create an apartment"""
        serializer = ApartmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'details':serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            serializer.save()
            return Response(
                {'details':'Apartment succesfully added', 'code':200},
                status=status.HTTP_200_OK
            )        
        except Exception as exception:
            return self._unknown_exception(exception)

    def list_apartments(self, request):
        """lists all apartments"""
        try:
            queryset = Apartments.objects.all()
            serializer = ReadApartmentSerializer(queryset, many=True)
            if not serializer.data:
                return Response(
                    {'details':'No apartments added to database yet.', 'code':400},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)
        
    def update_apartment(self, request, apartment_id):
        """update an apartment"""
        try:
            serializer = ApartmentSerializerNoPhoto(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'details':serializer.errors, 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            apartment = Apartments.objects.filter(apartmentID=apartment_id)
            
            if apartment:
                apartment.update(**serializer.data)
                return Response(
                    {'details':'Apartment succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':'Apartment to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            if type(exception).__name__ == 'IntegrityError':
                return Response(
                    {
                        'details':'Unknown error occured while adding apartment. Please try again.',
                        'code':400
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':str(exception), 'code':500}
            )

    def delete_apartment(self, apartment_id):
        """deletes an apartment"""
        try:
            apartment = Apartments.objects.get(apartmentID=apartment_id)
            self.bucket_name = 'krypto-files'
            self.object_name = 'media/profile/apartments/'+str(apartment.apartmentAvatar)

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
            Apartments.objects.filter(apartmentID=apartment_id).delete()
            return Response(
                {'details':'Succesfully deleted Apartment.', 'code':200},
                status=status.HTTP_200_OK
            )
        except:
            Apartments.objects.filter(apartmentID=apartment_id).delete()
            return Response(
                {'details':'Succesfully deleted Apartment.', 'code':200},
                status=status.HTTP_200_OK
            )
 
    def update_avatar(self, request):
        try:
            serializer = ApartmentSerializerPhoto(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'details':serializer.errors, 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )

            apartment = Apartments.objects.get(apartmentID=serializer.validated_data['apartmentID'])
            
            if apartment:
                apartment.apartmentAvatar = request.FILES['apartmentAvatar']
                apartment.save()
                return Response(
                    {'details':'Apartment succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':'Apartment to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )
        except Apartments.DoesNotExist:
            return Response(
                {'details': 'Apartment does not exist', 'code': 400},
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

    def retrieve_apartment(self, apartment_id):
        """retrieve a single apartment"""
        try:
            queryset = Apartments.objects.get(apartmentID=apartment_id)
            serializer = ReadApartmentSerializer(queryset)
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Apartments.DoesNotExist:
            return Response(
                {'details':'Apartment Does Not Exist', 'code': 400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)

    def retrieve_apartment_caretaker(self, caretaker_id):
        try:
            if not caretaker_id:
                return Response(
                    {'details':'Caretaker ID not provided', 'code':200},
                    status=status.HTTP_200_OK
                )

            queryset = Apartments.objects.filter(caretaker=caretaker_id)
            serializer = ReadApartmentSerializer(queryset, many=True)
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )

            
        except Apartments.DoesNotExist:
            return Response(
                {'details': 'Caretaker does not exist', 'code': 400},
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