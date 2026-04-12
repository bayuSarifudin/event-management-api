from rest_framework import serializers
from .models import Session, Event, Track

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

    def validate(self, data):
        track = data['track']
        start_time = data['start_time']
        end_time = data['end_time']
        
        event = track.event

        # basic time validation
        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")
        
        # within event date
        if start_time < event.start_date or end_time > event.end_date:
            raise serializers.ValidationError("Session must be within event date range.")

        # Check conflicts
        conflicts = Session.objects.filter(
            track=track,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        # exclude self when there is update
        if self.instance:
            conflicts = conflicts.exclude(id=self.instance.id)

        if conflicts.exists():
            raise serializers.ValidationError("Session time conflicts with another session in the same track.")

        return data

class TrackSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(many=True, read_only=True)
    class Meta:
        model = Track
        fields = '__all__'
        
class EventSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    available_seats = serializers.IntegerField(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_by']

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("Event end date must be after start date.")
        return data