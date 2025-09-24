from django.urls import path

from authentication.login.views import LoginView

from authentication.register.views import (
    RegisterView,
    MailVerificationView,
    SendMailVerificationView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register-user"),
    path("verify-email/", MailVerificationView.as_view(), name="verify-email"),
    path("send-verify-email/", SendMailVerificationView.as_view(), name="verify-email"),
]
