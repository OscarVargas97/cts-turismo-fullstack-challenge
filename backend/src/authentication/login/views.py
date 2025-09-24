from app.jwt.views import CookieTokenObtainPairView


class LoginView(CookieTokenObtainPairView):
    is_required_mail_otp = True
    email_subject = "Token de acceso"
