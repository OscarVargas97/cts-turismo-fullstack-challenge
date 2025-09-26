from rest_framework import serializers
from .models import Prize, Raffle, RafflePrize, Participant, Winner
from django.utils import timezone  # << correct import
from django.db.models import F
from django.db import transaction
from .models import Participant


class ParticipantUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)

    class Meta:
        model = Participant
        fields = ["id", "username", "email", "phone_number", "registration_date"]


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = ["id", "name", "description", "quantity", "image"]


class RafflePrizeSerializer(serializers.ModelSerializer):
    prize_details = PrizeSerializer(source="prize", read_only=True)

    class Meta:
        model = RafflePrize
        fields = [
            "id",
            "raffle",
            "prize",
            "quantity",
            "winners_selected",
            "prize_details",
        ]


class RaffleSerializer(serializers.ModelSerializer):
    prizes = RafflePrizeSerializer(many=True, read_only=True, source="raffleprize_set")

    class Meta:
        model = Raffle
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "status",
            "max_participants",
            "prize_description",
            "prizes",
        ]


class WinnerSerializer(serializers.ModelSerializer):
    participant_user_id = serializers.IntegerField(
        source="participant.user_id", read_only=True
    )
    prize_name = serializers.CharField(source="prize.prize.name", read_only=True)

    class Meta:
        model = Winner
        fields = [
            "id",
            "raffle",
            "participant",
            "prize",
            "drawn_date",
            "prize_claimed",
            "claim_date",
            "participant_user_id",
            "prize_name",
        ]
        read_only_fields = (
            "drawn_date",
            "claim_date",
            "participant_user_id",
            "prize_name",
        )

    def validate(self, data):
        raffle = data.get("raffle") or getattr(self.instance, "raffle", None)
        participant = data.get("participant") or getattr(
            self.instance, "participant", None
        )
        prize = data.get("prize") or getattr(self.instance, "prize", None)

        if not (raffle and participant and prize):
            return data

        if participant.raffle_id != raffle.id:
            raise serializers.ValidationError(
                {"participant": "El participante no pertenece a este sorteo."}
            )
        if prize.raffle_id != raffle.id:
            raise serializers.ValidationError(
                {"prize": "El premio no pertenece a este sorteo."}
            )

        if getattr(participant, "is_active", True) is False:
            raise serializers.ValidationError(
                {"participant": "El participante no está activo."}
            )

        if self.instance is None and prize.winners_selected >= prize.quantity:
            raise serializers.ValidationError(
                {
                    "prize": "Ya se han seleccionado todos los ganadores para este premio."
                }
            )

        if (
            self.instance is None
            and Winner.objects.filter(
                raffle=raffle, participant=participant, prize=prize
            ).exists()
        ):
            raise serializers.ValidationError(
                {
                    "non_field_errors": "Este participante ya es ganador de este premio en este sorteo."
                }
            )

        return data

    @transaction.atomic
    def create(self, validated_data):
        prize: RafflePrize = validated_data["prize"]
        updated = RafflePrize.objects.filter(
            pk=prize.pk, winners_selected__lt=F("quantity")
        ).update(winners_selected=F("winners_selected") + 1)
        if updated == 0:
            raise serializers.ValidationError(
                {"prize": "No quedan unidades disponibles de este premio."}
            )

        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        prize_claimed = validated_data.get("prize_claimed", instance.prize_claimed)

        if prize_claimed and not instance.prize_claimed:
            validated_data["claim_date"] = timezone.now()
        elif not prize_claimed and instance.prize_claimed:
            validated_data["claim_date"] = None

        return super().update(instance, validated_data)
