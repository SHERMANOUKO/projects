from rest_framework import serializers
from mails.models import Accounts


class AccountsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accounts
        fields = ('accountEmail', 'accountHolderName')

