from django.urls import path
from .views import (
    RaffleActivate,
    JoinRaffle,
    NewWinnerView,
    ActiveRaffleParticipantsView,
)

urlpatterns = [
    path(
        "raffles/<uuid:uuid>/activate/",
        RaffleActivate.as_view(),
        name="raffle-activate",
    ),
    path("get-winner/", NewWinnerView.as_view(), name="get-new-winner"),
    path("join/", JoinRaffle.as_view(), name="join-raffle"),
    path(
        "participation/", ActiveRaffleParticipantsView.as_view(), name="participation"
    ),
]
