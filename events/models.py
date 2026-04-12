from django.db import models
from django.conf import settings

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
      
class Track(models.Model):
    name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tracks')

    def __str__(self):
        return self.name

class Session(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    speaker_name = models.CharField(max_length=255)

    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='sessions')

    def __str__(self):
        return self.title