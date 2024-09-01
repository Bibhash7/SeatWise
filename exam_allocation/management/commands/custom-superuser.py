import os
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="bib").exists():
            User.objects.create_superuser(
                username="bib",
                email="",
                password="password"
            )