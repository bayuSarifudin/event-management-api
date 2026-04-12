from django.shortcuts import render
from rest_framework import generics
from .serializers import RegisterSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from events.permissions import IsSuperAdmin

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