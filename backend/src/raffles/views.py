from django.core.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework import status, serializers as drf_serializers
from typing import Optional
from django.db.models import F
import random
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from emails.mixins import TemplateEmailMixin
from django.conf import settings


from .models import (
    Participant,
    Prize,
    Raffle,
    RafflePrize,
    RaffleStatus,
    Winner,
)
from .serializer import (
    ParticipantUserSerializer,
    RaffleSerializer,
    WinnerSerializer,
)


class IsSuperAdmin:
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # número de items por página por defecto
    page_size_query_param = "page_size"
    max_page_size = 100


class RaffleActivate(GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Raffle.objects.all()
    lookup_field = "uuid"

    def post(self, request, *args, **kwargs):
        try:
            raffle = self.get_object()
            raffle.activate()
            return Response({"message": "Sorteo activado exitosamente"})
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NewWinnerView(TemplateEmailMixin, GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = WinnerSerializer
    template_key = "winner"
    template_context = {}  # <- Añadir esta línea

    def _get_active_raffle(self) -> Raffle:
        raffle = (
            Raffle.objects.filter(status=RaffleStatus.ACTIVE)
            .order_by("-created_at")
            .first()
        )
        if not raffle:
            raise drf_serializers.ValidationError(
                "No hay un sorteo activo en este momento."
            )
        return raffle

    def _pick_prize(self, raffle: Raffle, prize_id: Optional[int]) -> RafflePrize:
        qs_available = RafflePrize.objects.filter(
            raffle=raffle, winners_selected__lt=F("quantity")
        )

        if prize_id:
            prize = qs_available.filter(pk=prize_id).first()
            if not prize:
                raise drf_serializers.ValidationError(
                    {
                        "prize": "El premio indicado no existe o no tiene cupos disponibles."
                    }
                )
            return prize

        prizes = list(qs_available)
        if not prizes:
            raise drf_serializers.ValidationError(
                "No quedan premios con cupos disponibles en este sorteo."
            )
        return random.choice(prizes)

    def _pick_participant(self, raffle: Raffle, prize: RafflePrize) -> Participant:
        already_winner_ids = Winner.objects.filter(
            raffle=raffle, prize=prize
        ).values_list("participant_id", flat=True)
        eligible_qs = Participant.objects.filter(raffle=raffle, is_active=True).exclude(
            id__in=already_winner_ids
        )

        # Para grandes volúmenes, convendría una selección random más eficiente.
        # Aquí mantenemos simple:
        count = eligible_qs.count()
        if count == 0:
            raise drf_serializers.ValidationError(
                "No hay participantes elegibles para este premio."
            )

        # Selección aleatoria por índice para evitar ORDER BY ? (costoso en algunos DB)
        rand_index = random.randrange(count)
        return eligible_qs[rand_index]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        prize_id = request.query_params.get("prize_id") or request.data.get("prize_id")
        prize_id = int(prize_id) if prize_id is not None else None

        raffle = self._get_active_raffle()
        prize = self._pick_prize(raffle, prize_id)
        ATTEMPTS = 3
        last_error = None

        for _ in range(ATTEMPTS):
            try:
                participant = self._pick_participant(raffle, prize)
                payload = {
                    "raffle": raffle.pk,
                    "participant": participant.pk,
                    "prize": prize.pk,
                }
                user = participant.user

                serializer = self.get_serializer(data=payload)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
                self.destination_email = [user.email]
                self.from_email = settings.EMAIL_HOST_USER
                self.destination_email = [user.email]
                self._handle_email(request)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except drf_serializers.ValidationError as e:
                detail = e.detail
                if isinstance(detail, dict) and "non_field_errors" in detail:
                    last_error = e
                    continue
                raise

        if last_error is not None:
            raise last_error

        return Response(
            {"detail": "No fue posible asignar un ganador en este momento."},
            status=status.HTTP_409_CONFLICT,
        )


class JoinRaffle(GenericAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = RaffleSerializer

    def post(self, request):
        try:
            active_raffle = Raffle.objects.get(status=RaffleStatus.ACTIVE)

            if Participant.objects.filter(
                user=request.user, raffle=active_raffle
            ).exists():
                raise ValidationError("Ya estás participando en este sorteo")

            if active_raffle.max_participants:
                current_participants = Participant.objects.filter(
                    raffle=active_raffle
                ).count()
                if current_participants >= active_raffle.max_participants:
                    raise ValidationError(
                        "El sorteo ha alcanzado el límite de participantes"
                    )

            Participant.objects.create(user=request.user, raffle=active_raffle)

            return Response(
                {
                    "message": "Te has registrado exitosamente en el sorteo",
                    "raffle": self.get_serializer(active_raffle).data,
                }
            )

        except Raffle.DoesNotExist:
            return Response(
                {"error": "No hay sorteos activos en este momento"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ActiveRaffleParticipantsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ParticipantUserSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        raffle = (
            Raffle.objects.filter(status=RaffleStatus.ACTIVE)
            .order_by("-created_at")
            .first()
        )

        if not raffle:
            raise NotFound("No hay un sorteo activo actualmente.")

        return (
            Participant.objects.filter(
                raffle=raffle, is_active=True, user__is_active=True
            )
            .select_related("user")
            .order_by("registration_date")
        )
