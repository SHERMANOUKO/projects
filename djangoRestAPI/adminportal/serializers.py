from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from adminportal.models import CustomUser, Regions, Agents, Branches, Landlords, \
    Caretakers, Apartments

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'user_type']
        extra_kwargs = {
            'username' : {
                'validators':[UnicodeUsernameValidator()]
            }
        }

class MinifiedUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type']

class LoginFeedbackSerializer(serializers.Serializer):
    usertype = serializers.CharField()
    expires_in = serializers.IntegerField()
    superadmin = serializers.BooleanField()
    token = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RegionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Regions
        fields = ['regionID', 'regionName', 'regionCounty']
        extra_kwargs = {
            'regionName': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

class AgentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agents
        fields = ['agentID', 'username', 'agentNationalID', 'agentName', 'agentAvatar', 'agentPhoneNumber']
        extra_kwargs = {
            'agentNationalID':{
                'validators': [UnicodeUsernameValidator()]
            },
            'agentPhoneNumber':{
                'validators':[UnicodeUsernameValidator]
            },
            'username':{
                'validators':[UnicodeUsernameValidator]
            }
        }

class ReadAgentsSerializer(serializers.ModelSerializer):
    username = MinifiedUserSerializer(read_only=True)

    class Meta:
        model = Agents
        fields = ['agentID', 'username', 'agentNationalID', 'agentName', 'agentAvatar', 'agentPhoneNumber']
        extra_kwargs = {
            'agentNationalID':{
                'validators': [UnicodeUsernameValidator()]
            },
            'agentPhoneNumber':{
                'validators':[UnicodeUsernameValidator]
            },
            'username':{
                'validators':[UnicodeUsernameValidator]
            }
        }

class AgentsSerializerNoPhoto(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agents
        fields = ['agentID', 'agentNationalID', 'agentName', 'agentPhoneNumber']
        extra_kwargs = {
            'agentNationalID':{
                'validators': [UnicodeUsernameValidator()]
            },
            'agentPhoneNumber':{
                'validators':[UnicodeUsernameValidator]
            }
        }

class AgentsSerializerPhoto(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agents
        fields = ['agentNationalID', 'agentAvatar']
        extra_kwargs = {
            'agentNationalID':{
                'validators': [UnicodeUsernameValidator()]
            }
        }

class MinifiedAgentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agents
        fields = ['agentName', 'agentPhoneNumber']

class BranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = [
            'region',
            'agent',
            'branchName',
            'branchEmailAddress',
            'branchPhoneNumber',
            'branchBuildingLocation',
            'branchLatitude',
            'branchLongitude'
        ]
        extra_kwargs = {
            'branchEmailAddress':{
                'validators': [UnicodeUsernameValidator]
            },
            'branchPhoneNumber':{
                'validators':[UnicodeUsernameValidator]
            },
            'agent':{
                'validators':[UnicodeUsernameValidator]
            }
        }

class ReadBranchesSerializer(serializers.HyperlinkedModelSerializer):
    region = RegionsSerializer(read_only=True)
    agent = MinifiedAgentsSerializer(read_only=True)

    class Meta:
        model = Branches
        fields = [
            'branchID',
            'region',
            'branchName',
            'agent',
            'branchEmailAddress',
            'branchPhoneNumber',
            'branchBuildingLocation',
            'branchLatitude',
            'branchLongitude'
        ]

class CaretakerBranchesSerializer(serializers.HyperlinkedModelSerializer):
    region = RegionsSerializer(read_only=True)

    class Meta:
        model = Branches
        fields = [
            'region',
            'branchName',
            'branchPhoneNumber'
        ]

class LandlordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Landlords
        fields = [
            'landlordID',
            'username',
            'landlordNationalID',
            'landlordEmailAddress',
            'landlordPrimaryPhoneNumber',
            'landlordSecondaryPhoneNumber',
            'landlordAvatar',
            'landlordName'
        ]
        extra_kwargs = {
            'landlordNationalID':{
                'validators': [UnicodeUsernameValidator()]
            },
            'landlordPrimaryPhoneNumber':{
                'validators':[UnicodeUsernameValidator]
            },
            'landlordSecondaryPhoneNumber':{
                'validators':[UnicodeUsernameValidator]
            },
            'landlordEmailAddress':{
                'validators':[UnicodeUsernameValidator]
            },
            'username':{
                'validators': [UnicodeUsernameValidator()]
            },
        }

class LandlordsSerializerNoPhoto(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Landlords
        fields = [ 
            'landlordEmailAddress', 
            'landlordPrimaryPhoneNumber',
            'landlordSecondaryPhoneNumber',
            'landlordName'
        ]
        extra_kwargs = {
            'landlordPrimaryPhoneNumber':{
                'validators':[UnicodeUsernameValidator]
            },
            'landlordSecondaryPhoneNumber':{
                'validators':[UnicodeUsernameValidator]
            },
            'landlordEmailAddress':{
                'validators':[UnicodeUsernameValidator]
            }
        }

class LandlordSerializerPhoto(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Landlords
        fields = ['landlordNationalID', 'landlordAvatar']
        extra_kwargs = {
            'landlordNationalID':{
                'validators': [UnicodeUsernameValidator()]
            }
        }

class CaretakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caretakers
        fields = [
            'caretakerID',
            'username',
            'caretakerNationalID',
            'caretakerPhoneNumber',
            'caretakerAvatar',
            'caretakerName',
            'branch'
        ]
        extra_kwargs = {
            'caretakerNationalID':{
                'validators': [UnicodeUsernameValidator()]
            },
            'caretakerPhoneNumber':{
                'validators':[UnicodeUsernameValidator]
            }
        }

class CaretakerSerializerNoPhoto(serializers.ModelSerializer):
    class Meta:
        model = Caretakers
        fields = [
            'caretakerName',
            'caretakerPhoneNumber',
            'branch'
        ]
        extra_kwargs = {
            'caretakerPhoneNumber':{
                'validators':[UnicodeUsernameValidator]
            }
        }

class CaretakerSerializerPhoto(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Caretakers
        fields = ['caretakerNationalID', 'caretakerAvatar']
        extra_kwargs = {
            'caretakerNationalID':{
                'validators': [UnicodeUsernameValidator()]
            }
        }

class ReadCaretakerSerializer(serializers.HyperlinkedModelSerializer):
    branch = CaretakerBranchesSerializer()

    class Meta:
        model = Caretakers
        fields = [
            'caretakerID',
            'username',
            'caretakerNationalID',
            'caretakerPhoneNumber',
            'caretakerAvatar',
            'caretakerName',
            'branch'
        ]
        extra_kwargs = {
            'caretakerNationalID':{
                'validators': [UnicodeUsernameValidator()]
            },
            'caretakerPhoneNumber':{
                'validators':[UnicodeUsernameValidator]
            }
        }

class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartments
        fields = [
            'apartmentID',
            'landlord',
            'apartmentName',
            'apartmentCounty',
            'apartmentEstate',
            'branch',
            'apartmentLatitude',
            'apartmentLongitude',
            'apartmentStudentType',
            'caretaker',
            'apartmentAvatar'
        ]

class ReadApartmentSerializer(serializers.ModelSerializer):
    branch = CaretakerBranchesSerializer()
    

    class Meta:
        model = Apartments
        fields = [
            'apartmentID',
            'landlord',
            'apartmentName',
            'apartmentCounty',
            'apartmentEstate',
            'branch',
            'apartmentLatitude',
            'apartmentLongitude',
            'apartmentStudentType',
            'caretaker',
            'apartmentAvatar'
        ]

class ApartmentSerializerNoPhoto(serializers.ModelSerializer):
    class Meta:
        model = Apartments
        fields = [
            'apartmentID',
            'landlord',
            'apartmentName',
            'apartmentStudentType',
            'caretaker'
        ]

class ApartmentSerializerPhoto(serializers.ModelSerializer):
    class Meta:
        model = Apartments
        fields = ['apartmentID', 'apartmentAvatar']
