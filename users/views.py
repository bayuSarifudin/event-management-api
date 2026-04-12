from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .serializers import RegisterSerializer, UserSerializer

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from events.permissions import IsSuperAdmin
from core.responses import paginated_response

# Create your views here.
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class PromoteToAdminView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request):
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
            user.role = 'admin'
            user.save()

            return Response({
                "message": "User promoted to admin"
            })

        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=404)
            
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginated_response(
                self.paginator,
                serializer.data,
                message="List of users"
            )

        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message="List of users"
        )