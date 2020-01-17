"""Handles region related requests"""
from rest_framework.response import Response
from rest_framework import status
from adminportal.models import Regions
from adminportal.serializers import RegionsSerializer


class RegionsController():
    """handles regions related requests"""

    def _unknown_exception(self, exception):
        """Returns an unanticipated exception"""
        return Response(
            {'details':str(exception), 'code': 500},
            status=status.HTTP_200_OK
        )

    def create_region(self, request):
        """creates a new region"""
        regions_serializer = RegionsSerializer(data=request.data)
        if not regions_serializer.is_valid():
            return Response(
                {'details':regions_serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            Regions.objects.get(regionName=regions_serializer.validated_data['regionName'])
            return Response(
                {'details':'Region Name Already Exists', 'code':400},
                status=status.HTTP_200_OK
            )
        except Regions.DoesNotExist:
            regions_serializer.save()
            return Response(
                {'details':'Region succesfully created', 'code':200},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)

    def list_regions(self, request):
        """lists all regions"""
        try:
            queryset = Regions.objects.all()
            serializer = RegionsSerializer(queryset, many=True)
            if not serializer.data:
                return Response(
                    {'details':'No Regions added to database yet.', 'code':400},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)

    def retrieve_region(self, region_id):
        """retrieve a single region"""
        try:
            queryset = Regions.objects.get(regionID=region_id)
            serializer = RegionsSerializer(queryset)
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Regions.DoesNotExist:
            return Response(
                {'details':'Region Does Not Exist', 'code': 400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)

    def update_region(self, request, region_id):
        """update a region"""
        try:
            serializer = RegionsSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'details':serializer.errors, 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            region = Regions.objects.filter(regionID=region_id)
            
            if region:
                region.update(**serializer.data)
                return Response(
                    {'details':'Region succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':'Region to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            if type(exception).__name__ == 'IntegrityError':
                return Response(
                    {
                        'details':'Another region already has '\
                                    'the region name you are trying to use',
                        'code':400
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':str(exception), 'code':500}
            )

    def delete_region(self, region_id):
        """deletes a given region"""
        Regions.objects.filter(regionID=region_id).delete()
        return Response(
            {'details':'Succesfully deleted region.', 'code':200},
            status=status.HTTP_200_OK
        )