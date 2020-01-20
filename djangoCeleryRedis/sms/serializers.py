from rest_framework import serializers
from sms.models import ScheduledDispatch


class DispatchSmsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduledDispatch
        fields = ('dispatchRecipient', 'dispatchItem')
