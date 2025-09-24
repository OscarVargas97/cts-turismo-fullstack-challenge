from django.urls import path

from authentication.login.views import LoginView

from authentication.register.views import (
    RegisterView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register-user"),
]
