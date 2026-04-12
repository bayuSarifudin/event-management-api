from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Registration
from .serializers import RegistrationSerializer
from rest_framework.permissions import IsAuthenticated

class RegistrationViewSet(ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)