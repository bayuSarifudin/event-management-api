from django.db import models
from django.db import models
from django.conf import settings

user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)
from events.models import Event

# Create your models here.

class Registration(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')