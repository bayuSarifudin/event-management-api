from rest_framework import serializers
from .models import Registration
from events.models import Event

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'event', 'registered_at']
        read_only_fields = ['id', 'registered_at']

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