from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from sms.serializers import DispatchSmsSerializer
from sms.models import ScheduledDispatch

class ScheduleDispatchSms(CreateAPIView):
    serializer_class = DispatchSmsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'Dispatch scheduled succesfully',
            }
        
        return Response(response, status=status_code)

