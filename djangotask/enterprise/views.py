from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Department, Positions, Worker, PosHistory, VacHistory
from .serializers import DepartmentSerializer, PositionsSerializer, WorkerSerializer, \
    PosHistorySerializer, VacHistorySerializer, FirstTaskSerializer, SecondTaskSerializer,\
    ThirdTaskSerializer, FourthTaskSerializer, LoginSerializer, RegistrationSerializer, UserSerializer
from .renderers import UserJSONRenderer


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer, BrowsableAPIRenderer)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer, BrowsableAPIRenderer)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer, BrowsableAPIRenderer)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class PositionsViewSet(viewsets.ModelViewSet):
    serializer_class = PositionsSerializer
    queryset = Positions.objects.all()


class WorkerViewSet(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()


class PosHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = PosHistorySerializer
    queryset = PosHistory.objects.all()


class VacHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = VacHistorySerializer
    queryset = VacHistory.objects.all()


class FirstTaskViewSet(viewsets.ModelViewSet):
    serializer_class = FirstTaskSerializer
    queryset = Department.objects.all()


class SecondTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SecondTaskSerializer
    queryset = Worker.objects.all()


class ThirdTaskViewSet(viewsets.ModelViewSet):
    serializer_class = ThirdTaskSerializer
    queryset = Worker.objects.all()


class FourthTaskViewSet(viewsets.ModelViewSet):
    serializer_class = FourthTaskSerializer
    queryset = Department.objects.all()
