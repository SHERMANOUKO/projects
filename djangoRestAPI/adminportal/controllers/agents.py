import os
from rest_framework.response import Response
from rest_framework import status
import boto3
from django.http import FileResponse
from adminportal.serializers import AgentsSerializer, ReadAgentsSerializer, AgentsSerializerNoPhoto, AgentsSerializerPhoto
from adminportal.models import Agents
from adminportal.services.filename import randomString


class AgentsController():
    """Handles agents request"""

    def _unknown_exception(self, exception):
        """Returns an unanticipated exception"""
        return Response(
            {'details':str(exception), 'code': 500},
            status=status.HTTP_200_OK
        )

    def create_agent(self, request):
        """creates an agent"""
        serializer = AgentsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'details':serializer.errors, 'code':400},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if 'username' in serializer.validated_data:
            try:
                Agents.objects.get(username=serializer.validated_data['username'])
                return Response(
                    {'details':'Agent with that username Already Exists', 'code':400},
                    status=status.HTTP_200_OK
                )
            except Agents.DoesNotExist:
                pass

        try:
            Agents.objects.get(agentPhoneNumber=serializer.validated_data['agentPhoneNumber'])
            return Response(
                {'details':'Agent Phone Number Already Exists', 'code':400},
                status=status.HTTP_200_OK
            )
        except Agents.DoesNotExist:
            try:
                Agents.objects.get(agentNationalID=serializer.validated_data['agentNationalID'])
                return Response(
                    {'details':'Agent National ID Already Exists', 'code':400},
                    status=status.HTTP_200_OK
                )
            except Agents.DoesNotExist:
                # Agents.objects.create(**serializer.validated_data)
                serializer.save()
                return Response(
                    {'details':'Agent succesfully created', 'code':200},
                    status=status.HTTP_200_OK
                )
            except Exception as exception:
                return self._unknown_exception(exception)
        except Exception as exception:
            return self._unknown_exception(exception)

    def list_agents(self, request):
        """lists all agents"""
        try:
            queryset = Agents.objects.all()
            serializer = ReadAgentsSerializer(queryset, many=True)
            if not serializer.data:
                return Response(
                    {'details':'No Agents added to database yet.', 'code':400},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)

    def get_avatar(self, request, agent_id):
        """get one photo"""
        try:
            agent = Agents.objects.get(agentID=agent_id)
            filename = randomString() + str(agent.agentAvatar)
            
            self.s3 = boto3.client(
                's3',
                aws_access_key_id='AKIAVJ3LWIU3CRDMYUPF',
                aws_secret_access_key='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',
            )

            self.bucket_name = 'krypto-files'
            self.object_name = 'media/profile/agents/'+str(agent.agentAvatar)

            with open(filename, 'wb') as agent_avatar:
                self.s3.download_fileobj(self.bucket_name, self.object_name, agent_avatar)
            
            file = open(filename, 'rb')
            os.remove(filename)
            return FileResponse(file)
        except Exception:
            # if type(e).__name__ == 'ClientError':
            return Response()

    def delete_agent(self, agent_id):
        """deletes an agent"""
        try:
            agent = Agents.objects.get(agentID=agent_id)
            self.bucket_name = 'krypto-files'
            self.object_name = 'media/profile/agents/'+str(agent.agentAvatar)

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
            Agents.objects.filter(agentID=agent_id).delete()
            return Response(
                {'details':'Succesfully deleted agent.', 'code':200},
                status=status.HTTP_200_OK
            )
        except:
            Agents.objects.filter(agentID=agent_id).delete()
            return Response(
                {'details':'Succesfully deleted agent.', 'code':200},
                status=status.HTTP_200_OK
            )
 
    def update_agent(self, request, agent_id):
        try:
            serializer = AgentsSerializerNoPhoto(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'details':serializer.errors, 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            agent = Agents.objects.filter(agentID=agent_id)
            
            if agent:
                agent.update(**serializer.data)
                return Response(
                    {'details':'Agent succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':'Agent to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            if type(exception).__name__ == 'IntegrityError':
                return Response(
                    {
                        'details':'Another agent already has '\
                                    'the phone number or national ID you are trying to use',
                        'code':400
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':str(exception), 'code':500}
            )

    def retrieve_agent(self, agent_id):
        """retrieve one agent"""
        try:
            queryset = Agents.objects.get(agentID=agent_id)
            serializer = ReadAgentsSerializer(queryset)
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Agents.DoesNotExist:
            return Response(
                {'details':'Agent Does Not Exist', 'code': 400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)

    def update_avatar(self, request):
        try:
            serializer = AgentsSerializerPhoto(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'details':serializer.errors, 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )

            agent = Agents.objects.get(agentNationalID=serializer.validated_data['agentNationalID'])
            
            if agent:
                agent.agentAvatar = request.FILES['agentAvatar']
                agent.save()
                return Response(
                    {'details':'Agent succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':'Agent to be updated does not exist', 'code':400},
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
