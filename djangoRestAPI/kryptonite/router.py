from rest_framework import routers
from adminportal import views

router = routers.DefaultRouter()
router.register('customusers', views.UserViewset, basename='customusers')
router.register('regions', views.RegionsViewset, basename='regions')
router.register('agents', views.AgentsViewset, basename='agents')
router.register('branches', views.BranchesViewset, basename='branches')
router.register('landlords', views.LandlordsViewset, basename='landlords')
router.register('caretakers', views.CaretakersViewset, basename='caretakers')
router.register('apartments', views.ApartmentsViewset, basename='apartments')
