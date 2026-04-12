from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model


@receiver(post_migrate)
def create_default_superadmin(sender, **kwargs):
    User = get_user_model()

    if not User.objects.filter(username='superadmin').exists():
        User.objects.create_user(
            username='superadmin',
            password='P@ssw0rd',
            role='superadmin'
        )