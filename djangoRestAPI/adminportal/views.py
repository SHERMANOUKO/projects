from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from adminportal.custompermissions import CustomPermission, CustomAgentPermission, \
    CustomAgentCaretakerPermission, RegistrationPermission
from adminportal.controllers.users import UsersController
from adminportal.controllers.login import LoginController
from adminportal.controllers.regions import RegionsController
from adminportal.controllers.agents import AgentsController
from adminportal.controllers.branches import BranchesController
from adminportal.controllers.landlord import LandlordController
from adminportal.controllers.caretaker import CaretakerController
from adminportal.controllers.apartment import ApartmentController
from adminportal.serializers import CustomUserSerializer, MinifiedUserSerializer, LoginSerializer, \
    LoginFeedbackSerializer, RegionsSerializer, AgentsSerializer, AgentsSerializerNoPhoto, \
    AgentsSerializerPhoto, ReadBranchesSerializer, BranchesSerializer, LandlordSerializer, \
    LandlordSerializerPhoto, LandlordsSerializerNoPhoto, CaretakerSerializer, CaretakerSerializerNoPhoto, \
    CaretakerSerializerPhoto, ApartmentSerializer, ApartmentSerializerNoPhoto, ApartmentSerializerPhoto
    # Create your views here.

class UserViewset(viewsets.ViewSet):
    """User viewset"""
    lookup_field = 'username'
    
    @swagger_auto_schema(
        responses={200: MinifiedUserSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists users."
    )
    def list(self, request):
        """return all users"""    
        list_users = UsersController()
        return list_users.list_users(request)

    @swagger_auto_schema(
        request_body=CustomUserSerializer(),
        responses={200: CustomUserSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This creates a user."
    )
    def create(self, request):
        """create a user"""
        create_user = UsersController()
        return create_user.create_user(request)

    @swagger_auto_schema(
        responses={200: 'Succesfully deleted', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This deletes a user."
    )
    def destroy(self, request, username=None):
        """delete user"""
        delete_user = UsersController()
        return delete_user.delete_user(username)

    @swagger_auto_schema(
        request_body=CustomUserSerializer(),
        responses={200: 'Succesful update', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This updates a user."
    )
    def update(self, request, username=None):
        """update user"""
        update_user = UsersController()
        return update_user.update_user(request, username)

    @swagger_auto_schema(
        responses={200: MinifiedUserSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This retrievs a user."
    )
    def retrieve(self, request, username=None):
        """retrieve a user"""
        retrieve_user = UsersController()
        return retrieve_user.retrieve_user(username)

    @swagger_auto_schema(
        request_body=LoginSerializer(),
        responses={200: LoginFeedbackSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This creates a user."
    )
    @action(methods=['POST'], detail=False, permission_classes=[])
    def login(self, request):
        """login a user"""
        login_user = LoginController()
        return login_user.login(request)

    usertype_param = openapi.Parameter('usertype', openapi.IN_QUERY, type=openapi.TYPE_STRING)
    @swagger_auto_schema(
        responses={200: MinifiedUserSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This gets users of given usertype.",
        manual_parameters=[usertype_param]
    )
    @action(methods=['GET'], detail=False, )
    def getusersofsertype(self, request):
        """get users of given usertype"""
        usertype = request.GET.get('usertype', None)
        get_usertype_user = UsersController()
        return get_usertype_user.list_usertype_users(usertype)

    def get_permissions(self):
        if self.action == 'create':
            return [RegistrationPermission(), ]
        if self.action == 'list':
            return [CustomPermission(), ]
        return super(UserViewset, self).get_permissions()

class RegionsViewset(viewsets.ViewSet):
    """regions viewset"""
    lookup_field = 'regionID'

    @swagger_auto_schema(
        responses={200: RegionsSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists regions."
    )
    def list(self, request):
        """list all regions"""
        list_regions = RegionsController()
        return list_regions.list_regions(request)

    @swagger_auto_schema(
        request_body=RegionsSerializer(),
        responses={200: 'Succesfully created', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This creates a region."
    )
    def create(self, request):
        """create a region"""
        create_region = RegionsController()
        return create_region.create_region(request)

    @swagger_auto_schema(
        responses={200: RegionsSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This retrieves a region."
    )
    def retrieve(self, request, regionID=None):
        """retrieve a region"""
        retrieve_region = RegionsController()
        return retrieve_region.retrieve_region(regionID)

    @swagger_auto_schema(
        request_body=RegionsSerializer(),
        responses={200: 'Succesfully updated', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This updates a region."
    )
    def update(self, request, regionID=None):
        """update a region"""
        update_region = RegionsController()
        return update_region.update_region(request, regionID)

    @swagger_auto_schema(
        responses={200: 'Succesfully deleted', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This deletes a region."
    )
    def destroy(self, request, regionID=None):
        """delete a region"""
        delete_region = RegionsController
        return delete_region.delete_region(request, regionID)

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            return [CustomPermission(), ]
        return [IsAuthenticatedOrReadOnly(), ]

class AgentsViewset(viewsets.ViewSet):
    """Agents viewset"""
    lookup_field = 'agentID'
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        responses={200: AgentsSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def list(self, request):
        """list all agents"""
        list_agents = AgentsController()
        return list_agents.list_agents(request)

    @swagger_auto_schema(
        request_body=AgentsSerializer(),
        responses={200: 'Succesfully created', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This creates an agent."
    )
    def create(self, request):
        """Create an agent"""
        create_agent = AgentsController()
        return create_agent.create_agent(request)

    @swagger_auto_schema(
        request_body=AgentsSerializerNoPhoto(),
        responses={200: 'Succesfully updated', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This updates an agent."
    )
    def update(self, request, agentID=None):
        """update agent"""
        update_agent = AgentsController()
        return update_agent.update_agent(request, agentID)

    @swagger_auto_schema(
        responses={200: AgentsSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists one agent."
    )
    def retrieve(self, request, agentID=None):
        """retrieve an agent"""
        retrieve_agent = AgentsController()
        return retrieve_agent.retrieve_agent(agentID)

    @swagger_auto_schema(
        responses={200: 'Succesfully deleted', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This deletes an agent."
    )
    def destroy(self, request, agentID=None):
        """delete agent"""
        delete_agent = AgentsController
        return delete_agent.delete_agent(request, agentID)

    @swagger_auto_schema(
        responses={400: ''},
        operation_description="This gets agent avatar."
    )
    @action(methods=['GET'], detail=True)
    def getavatar(self, request, agentID=None):
        """get agent avatar"""
        one_pic = AgentsController()
        return one_pic.get_avatar(request, agentID)

    @swagger_auto_schema(
        request_body=AgentsSerializerPhoto(),
        responses={200: 'Succesfully updated', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This updates agents photo."
    )
    @action(methods=['POST'], detail=False, permission_classes=[CustomPermission, ])
    def updateavatar(self, request):
        """update agent avatar"""
        update_avatar = AgentsController()
        return update_avatar.update_avatar(request)

    def get_permissions(self):
        if self.action not in ('create', 'destroy', 'list', 'update'):
            return super(AgentsViewset, self).get_permissions()
        return [CustomPermission(), ]

class BranchesViewset(viewsets.ViewSet):
    """Branches viewset"""
    lookup_field = 'branchID'

    @swagger_auto_schema(
        responses={200: ReadBranchesSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def list(self, request):
        """list all branches"""
        list_branch = BranchesController()
        return list_branch.list_branches(request)

    @swagger_auto_schema(
        request_body=BranchesSerializer(),
        responses={200: 'Succesfully Created', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def create(self, request):
        """create a branch"""
        create_branch = BranchesController()
        return create_branch.create_branch(request)

    @swagger_auto_schema(
        request_body=BranchesSerializer(),
        responses={200: AgentsSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def update(self, request, branchID=None):
        """update a branch"""
        update_branch = BranchesController()
        return update_branch.update_branch(request, branchID)

    @swagger_auto_schema(
        responses={200: 'Succesfully deleted', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def destroy(self, request, branchID=None):
        """delete branch"""
        delete_branch = BranchesController
        return delete_branch.delete_branch(request, branchID)

    @swagger_auto_schema(
        responses={200: ReadBranchesSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def retrieve(self, request, branchID=None):
        """retrieve a region"""
        retrieve_branch = BranchesController()
        return retrieve_branch.retrieve_branch(branchID)

    username = openapi.Parameter('username', openapi.IN_QUERY, type=openapi.TYPE_STRING)
    @swagger_auto_schema(
        responses={200: ReadBranchesSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This gets users of given usertype.",
        manual_parameters=[username]
    )
    @action(methods=['GET'], detail=False)
    def getAgentBranches(self, request):
        """get agent branches"""
        username = request.GET.get('username', None)
        retrieve_agent_branch = BranchesController()
        return retrieve_agent_branch.retrieve_agent_branch(username)
    
    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            return [CustomPermission(), ]
        return [IsAuthenticatedOrReadOnly(), ]

class LandlordsViewset(viewsets.ViewSet):
    """landlords viewset"""
    lookup_field = 'landlordID'
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        responses={200: LandlordSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def list(self, request):
        """list all landlords"""
        list_landlords = LandlordController()
        return list_landlords.list_landlords(request)

    @swagger_auto_schema(
        request_body=LandlordSerializer(),
        responses={200: 'Succesfully created', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def create(self, request):
        """create a landlord"""
        list_landlords = LandlordController()
        return list_landlords.create_landlord(request)

    @swagger_auto_schema(
        request_body=LandlordsSerializerNoPhoto(),
        responses={200: 'Succesfully updated', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def update(self, request, landlordID=None):
        """update a landlord"""
        update_landlord = LandlordController()
        return update_landlord.update_landlord(request, landlordID)

    @swagger_auto_schema(
        responses={200: 'Succesfully deleted', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def destroy(self, request, landlordID=None):
        """delete landlord"""
        delete_landlord = LandlordController
        return delete_landlord.delete_landlord(request, landlordID)

    @swagger_auto_schema(
        responses={200: '', 400: ''},
        operation_description="This lists all agents."
    )
    @action(methods=['GET'], detail=True)
    def getavatar(self, request, landlordID):
        """get landlord avatar"""
        one_pic = LandlordController()
        return one_pic.get_avatar(request, landlordID)

    @swagger_auto_schema(
        request_body=LandlordSerializerPhoto(),
        responses={200: 'Succesfully updated', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    @action(methods=['POST'], detail=False, permission_classes=[CustomAgentPermission, ])
    def updateavatar(self, request):
        """update landlord avatar"""
        update_avatar = LandlordController()
        return update_avatar.update_avatar(request)

    @swagger_auto_schema(
        responses={200: LandlordSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def retrieve(self, request, landlordID=None):
        """retrieve a landlord"""
        retrieve_landlord = LandlordController()
        return retrieve_landlord.retrieve_landlord(landlordID)
    
    def get_permissions(self):
        if self.action not in ('create', 'destroy', 'list'):
            return super(LandlordsViewset, self).get_permissions()
        return [CustomAgentPermission(), ]

class CaretakersViewset(viewsets.ViewSet):
    """caretaker viewset"""
    lookup_field = 'caretakerID'
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        responses={200: CaretakerSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def list(self, request):
        """list all caretakers"""
        list_caretakers = CaretakerController()
        return list_caretakers.list_caretakers(request)

    @swagger_auto_schema(
        request_body=CaretakerSerializer(),
        responses={200: 'Succesfully created', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def create(self, request):
        """create a caretaker"""
        create_caretaker = CaretakerController()
        return create_caretaker.create_caretaker(request)

    @swagger_auto_schema(
        request_body=CaretakerSerializerNoPhoto(),
        responses={200: 'Succesfully updated', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def update(self, request, caretakerID=None):
        """update a caretaker"""
        update_caretaker = CaretakerController()
        return update_caretaker.update_caretaker(request, caretakerID)

    @swagger_auto_schema(
        responses={200: 'Succesfully deleted', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def destroy(self, request, caretakerID=None):
        """delete caretaker"""
        delete_caretaker = CaretakerController
        return delete_caretaker.delete_caretaker(request, caretakerID)

    @swagger_auto_schema(
        responses={200: '', 400: ''},
        operation_description="This lists all agents."
    )
    @action(methods=['GET'], detail=True)
    def getavatar(self, request, caretakerID=None):
        """get caretaker avatar"""
        one_pic = CaretakerController()
        return one_pic.get_avatar(request, caretakerID)

    @swagger_auto_schema(
        request_body=CaretakerSerializerPhoto(),
        responses={200: 'Succesfully updated', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    @action(methods=['POST'], detail=False, permission_classes=[CustomAgentPermission, ])
    def updateavatar(self, request):
        """update caretaker avatar"""
        update_avatar = CaretakerController()
        return update_avatar.update_avatar(request)

    @swagger_auto_schema(
        responses={200: CaretakerSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def retrieve(self, request, caretakerID=None):
        """retrieve a caretaker"""
        retrieve_caretaker = CaretakerController()
        return retrieve_caretaker.retrieve_caretaker(caretakerID)

    def get_permissions(self):
        if self.action not in ('create', 'destroy', 'list'):
            return super(CaretakersViewset, self).get_permissions()
        return [CustomAgentPermission(), ]
    
class ApartmentsViewset(viewsets.ViewSet):
    """apartments viewset"""
    lookup_field = 'apartmentID'
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        responses={200: ApartmentSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def list(self, request):
        """list all apartments"""
        list_apartments = ApartmentController()
        return list_apartments.list_apartments(request)

    @swagger_auto_schema(
        request_body=ApartmentSerializer(),
        responses={200: 'Succesfully created', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def create(self, request):
        """create an apartment"""
        create_apartments = ApartmentController()
        return create_apartments.create_apartment(request)

    @swagger_auto_schema(
        request_body=ApartmentSerializerNoPhoto(),
        responses={200: 'Succesfully updated', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def update(self, request, apartmentID=None):
        """update an apartment"""
        update_apartment = ApartmentController()
        return update_apartment.update_apartment(request, apartmentID)

    @swagger_auto_schema(
        responses={200: 'Succesfully deleted', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def destroy(self, request, apartmentID=None):
        """delete apartment"""
        delete_apartment = ApartmentController
        return delete_apartment.delete_apartment(request, apartmentID)

    @swagger_auto_schema(
        request_body=CaretakerSerializerPhoto(),
        responses={200: 'Succesfully updated', 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    @action(methods=['POST'], detail=False, permission_classes=[CustomAgentPermission, ])
    def updateavatar(self, request):
        """update apartment avatar"""
        update_avatar = LandlordController()
        return update_avatar.update_avatar(request)

    @swagger_auto_schema(
        responses={200: CaretakerSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This lists all agents."
    )
    def retrieve(self, request, apartmentID=None):
        """retrieve an apartment"""
        retrieve_apartment = ApartmentController()
        return retrieve_apartment.retrieve_apartment(apartmentID)

    caretaker = openapi.Parameter('caretakerID', openapi.IN_QUERY, type=openapi.TYPE_STRING)
    @swagger_auto_schema(
        responses={200: CaretakerSerializer(), 400: 'Unsuccesful / User error', 500:'Code error'},
        operation_description="This gets users of given usertype.",
        manual_parameters=[caretaker]
    )
    @action(methods=['GET'], detail=False, permission_classes=[])
    def apartmentcaretaker(self, request):
        """get caretaker apartments."""
        caretaker_id = request.GET.get('caretakerID')
        list_caretaker_apartments = ApartmentController()
        return list_caretaker_apartments.retrieve_apartment_caretaker(caretaker_id)

    def get_permissions(self):
        if self.action not in ('create', 'destroy', 'update'):
            return super(ApartmentsViewset, self).get_permissions()
        return [CustomAgentPermission(), ]

