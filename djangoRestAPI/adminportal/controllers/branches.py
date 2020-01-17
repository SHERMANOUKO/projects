from rest_framework import status
from rest_framework.response import Response
from adminportal.serializers import BranchesSerializer, ReadBranchesSerializer
from adminportal.models import Branches

class BranchesController():
    """handles branches requests"""

    def _unknown_exception(self, exception):
        """Returns an unanticipated exception"""
        return Response(
            {'details':str(exception), 'code': 500},
            status=status.HTTP_200_OK
        )

    def list_branches(self, request):
        """lists all agents"""
        try:
            queryset = Branches.objects.all()
            serializer = ReadBranchesSerializer(queryset, many=True)
            if not serializer.data:
                return Response(
                    {'details':'No Branches added to database yet.', 'code':400},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)

    def create_branch(self, request):
        """create a branch"""
        serializer = BranchesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'details':serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            Branches.objects.get(branchPhoneNumber=serializer.validated_data['branchPhoneNumber'])
            return Response(
                {'details':'Branch Phone Number Already Exists', 'code': 400},
                status=status.HTTP_200_OK
            )
        except Branches.DoesNotExist:
            try:
                Branches.objects.get(branchEmailAddress=serializer.validated_data['branchEmailAddress'])
                return Response(
                    {'details':'Branch Email Address Already Exists', 'code': 400},
                    status=status.HTTP_200_OK
                )
            except Branches.DoesNotExist:
                try:
                    Branches.objects.get(agent=serializer.validated_data['agent'])
                    return Response(
                        {'details':'Agent Already Has a Branch', 'code': 400},
                        status=status.HTTP_200_OK
                    )
                except Branches.DoesNotExist:
                    serializer.save()
                    return Response(
                        {'details':'Branch added succesfuully', 'code': 200},
                        status=status.HTTP_200_OK
                    )
                except Exception as exception:
                    return self._unknown_exception(exception)
            except Exception as exception:
                return self._unknown_exception(exception)

        except Exception as exception:
            return self._unknown_exception(exception)

    def delete_branch(self, branch_id):
        """deletes a branch"""
        Branches.objects.filter(branchID=branch_id).delete()
        return Response(
            {'details':'Succesfully deleted branch.', 'code':200},
            status=status.HTTP_200_OK
        )

    def update_branch(self, request, branch_id):
        """update region"""
        serializer = BranchesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'details':serializer.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )

        branch = Branches.objects.filter(branchID=branch_id)
        try:
            if branch:
                branch.update(**serializer.data)
                return Response(
                    {'details':'Branch succesfully updated', 'code':500},
                    status=status.HTTP_200_OK
                )
        
            return Response(
                {'details':'Branch to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )

        except Exception as exception:
            if type(exception).__name__ == 'IntegrityError':
                return Response(
                    {
                        'details':'Another Branch already has '\
                                    'the email or phone number you are trying to use',
                        'code':400
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'details':str(exception), 'code':500}
            )

    def retrieve_branch(self, branch_id):
        """retrieve one branch"""
        try:
            queryset = Branches.objects.get(branchID=branch_id)
            serializer = ReadBranchesSerializer(queryset)
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Branches.DoesNotExist:
            return Response(
                {'details':'Branch Does Not Exist', 'code': 400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)

    def retrieve_agent_branch(self, username):
        """retrieve agent branch"""
        try:
            queryset = Branches.objects.get(username=username)
            serializer = ReadBranchesSerializer(queryset)
            return Response(
                {'details':serializer.data, 'code':200},
                status=status.HTTP_200_OK
            )
        except Branches.DoesNotExist:
            return Response(
                {'details':'Agent has not been allocated any branch.', 'code': 400},
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return self._unknown_exception(exception)

