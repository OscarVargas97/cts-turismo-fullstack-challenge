from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from raffles.models import Prize, Raffle, RafflePrize
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Crea datos de ejemplo para un sorteo con un premio específico y lo activa"

    def handle(self, *args, **kwargs):
        try:
            # Crear el premio
            prize = Prize.objects.create(
                name="Escapada romántica de 2 noches con todo incluido en hotel para parejas",
                description=(
                    "Disfruta de una experiencia única pensada para dos. "
                    "Este premio incluye una estadía de 2 noches totalmente pagadas "
                    "en un hotel seleccionado, ideal para escapar de la rutina "
                    "y compartir momentos especiales en pareja. "
                    "Con un ambiente acogedor, comodidades exclusivas y atención personalizada, "
                    "podrán relajarse, disfrutar de la tranquilidad y crear recuerdos inolvidables."
                ),
                quantity=1,
            )
            self.stdout.write(self.style.SUCCESS(f"Premio creado: {prize.name}"))

            # Crear el sorteo
            start_date = timezone.now() + timedelta(seconds=5)  # empezará muy pronto
            end_date = start_date + timedelta(days=7)

            raffle = Raffle.objects.create(
                title="Sorteo Escapada Romántica",
                description="¡Participa y gana una increíble escapada romántica! Una experiencia única para compartir con tu pareja.",
                start_date=start_date,
                end_date=end_date,
                status="DRAFT",
                max_participants=100,
                prize_description="Premio exclusivo para parejas que buscan una experiencia inolvidable.",
            )
            self.stdout.write(self.style.SUCCESS(f"Sorteo creado: {raffle.title}"))

            # Asociar el premio al sorteo
            RafflePrize.objects.create(raffle=raffle, prize=prize, quantity=1)
            self.stdout.write(
                self.style.SUCCESS("Premio asociado exitosamente al sorteo")
            )

            # Activar el sorteo
            try:
                raffle.activate()
                self.stdout.write(
                    self.style.SUCCESS(f"Sorteo '{raffle.title}' activado exitosamente")
                )
            except ValidationError as ve:
                self.stdout.write(
                    self.style.ERROR(f"No se pudo activar el sorteo: {ve}")
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al crear los datos: {str(e)}"))
