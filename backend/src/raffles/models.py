from django.db import models
from django.core.exceptions import ValidationError
from app.public.models import BaseModel
from authentication.models import User
from datetime import timezone


class Prize(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="prizes/", null=True, blank=True)

    def __str__(self):
        return self.name


class RaffleStatus:
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"

    choices = [
        (DRAFT, "Draft"),
        (ACTIVE, "Active"),
        (FINISHED, "Finished"),
        (CANCELLED, "Cancelled"),
    ]


class Raffle(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=RaffleStatus.choices,
        default=RaffleStatus.DRAFT,
    )
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    prize_description = models.TextField()

    def clean(self):
        if self.status == RaffleStatus.ACTIVE:
            if not self.start_date or not self.end_date:
                raise ValidationError(
                    "Las fechas de inicio y fin son requeridas para activar el sorteo"
                )
            active_raffle = (
                Raffle.objects.filter(status=RaffleStatus.ACTIVE)
                .exclude(id=self.id)
                .exists()
            )

            if active_raffle:
                raise ValidationError(
                    "Ya existe un sorteo activo. Solo puede haber un sorteo activo a la vez."
                )

            # Validar fechas
            if self.end_date <= self.start_date:
                raise ValidationError(
                    "La fecha de finalización debe ser posterior a la fecha de inicio."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def activate(self):
        self.status = RaffleStatus.ACTIVE

        if not self.start_date:
            self.start_date = timezone.now()
        if not self.end_date:
            raise ValidationError(
                "Debes especificar una fecha de finalización para activar el sorteo."
            )

        self.clean()
        self.save(update_fields=["status", "start_date", "end_date"])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class RafflePrize(BaseModel):
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    winners_selected = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ["raffle", "prize"]

    def clean(self):
        if self.winners_selected > self.quantity:
            raise ValidationError(
                "El número de ganadores no puede ser mayor que la cantidad de premios."
            )


class Participant(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raffle = models.ForeignKey(
        Raffle, on_delete=models.CASCADE, related_name="participants"
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["user", "raffle"]
        ordering = ["registration_date"]


class Winner(BaseModel):
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name="winners")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    prize = models.ForeignKey(RafflePrize, on_delete=models.CASCADE)
    drawn_date = models.DateTimeField(auto_now_add=True)
    prize_claimed = models.BooleanField(default=False)
    claim_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["raffle", "participant", "prize"]
        ordering = ["-drawn_date"]

    def clean(self):
        if self.prize.winners_selected >= self.prize.quantity:
            raise ValidationError(
                "Ya se han seleccionado todos los ganadores para este premio."
            )

    def save(self, *args, **kwargs):
        self.clean()
        if not self.id:
            self.prize.winners_selected += 1
            self.prize.save()
        super().save(*args, **kwargs)
