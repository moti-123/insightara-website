"""
One-time admin password reset — for use on Render's free tier, which has no Shell access.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Resets or creates a superuser's password from RESET_ADMIN_USERNAME / RESET_ADMIN_PASSWORD env vars."

    def handle(self, *args, **options):
        username = os.environ.get("RESET_ADMIN_USERNAME")
        password = os.environ.get("RESET_ADMIN_PASSWORD")

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                "RESET_ADMIN_USERNAME / RESET_ADMIN_PASSWORD not set — skipping."
            ))
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"is_staff": True, "is_superuser": True},
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created new superuser '{username}' with the given password."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Password reset for existing user '{username}'."))