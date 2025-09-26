import time
from django.core.management import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Espera a que la base de datos esté lista antes de arrancar Django"

    def handle(self, *args, **options):
        self.stdout.write("⏳ Esperando a que la base de datos esté disponible...")

        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
                db_conn.ensure_connection()  # Fuerza la conexión real
            except OperationalError:
                self.stdout.write(
                    "❌ Base de datos no disponible, esperando 1 segundo..."
                )
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("✅ Base de datos disponible"))
