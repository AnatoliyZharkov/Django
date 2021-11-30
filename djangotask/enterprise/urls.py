from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import *


router = DefaultRouter()
router.register(r'departments', viewset=DepartmentViewSet, basename='departments')
router.register(r'positions', viewset=PositionsViewSet, basename='positions')
router.register(r'workers', viewset=WorkerViewSet, basename='workers')
router.register(r'pos_historys', viewset=PosHistoryViewSet, basename='pos_historys')
router.register(r'vac_historys', viewset=VacHistoryViewSet, basename='vac_historys')
router.register(r'first_task', viewset=FirstTaskViewSet, basename='first_task')
router.register(r'second_task', viewset=SecondTaskViewSet, basename='second_task')
router.register(r'third_task', viewset=ThirdTaskViewSet, basename='third_task')
router.register(r'fourth_task', viewset=FourthTaskViewSet, basename='fourth_task')

app_name = 'enterprise'
urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
]
