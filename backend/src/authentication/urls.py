from django.urls import path

from authentication.login.views import LoginView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
]
