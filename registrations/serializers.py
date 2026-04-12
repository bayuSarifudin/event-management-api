from rest_framework import serializers

from users.models import User
from .models import Registration

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class RegistrationSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Registration
        fields = ['id', 'event', 'user', 'registered_at']
        read_only_fields = ['id', 'user', 'registered_at']

    def validate(self, data):
        user = self.context['request'].user
        event = data['event']

        # Check duplicate
        if Registration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("User already registered for this event.")

        # Check capacity
        total_registered = Registration.objects.filter(event=event).count()
        if total_registered >= event.capacity:
            raise serializers.ValidationError("Event capacity exceeded.")

        return data