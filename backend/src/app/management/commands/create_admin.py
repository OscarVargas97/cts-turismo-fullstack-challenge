from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Crea y activa un superusuario con email, username y contraseña predefinidos"

    def handle(self, *args, **options):
        username = "admin"
        email = "adminuser@gmail.com"
        password = "Password123"

        User = get_user_model()

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f"Usuario con email '{email}' ya existe.")
            )
            return

        user = User.objects.create_superuser(
            email=email, password=password, username=username
        )

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Superusuario '{email}' creado, activado y con permisos de superadmin correctamente."
            )
        )
