from django.urls import path

from authentication.change_pasword.views import (
    ChangePasswordRequestView,
    ChangePasswordView,
)
from authentication.register.views import (
    RegisterView,
    MailVerificationView,
    SendMailVerificationView,
)
from app.jwt.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register-user"),
    path("verify-email/", MailVerificationView.as_view(), name="verify-email"),
    path("send-verify-email/", SendMailVerificationView.as_view(), name="verify-email"),
    path(
        "change-password-request/",
        ChangePasswordRequestView.as_view(),
        name="change-password",
    ),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
]
