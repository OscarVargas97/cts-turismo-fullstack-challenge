EMAIL_TEMPLATES = {
    "winner": {
        "winner": {
            "subject": "¡Felicidades! 🎉 Has ganado",
            "html_body": """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{subject}</title>
<style>
body {{ font-family: Arial, sans-serif; background-color: #f9fafb; margin: 0; padding: 0; }}
.container {{ max-width: 600px; margin: auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); overflow: hidden; }}
.header {{ background: linear-gradient(90deg, #4CAF50, #2E7D32); color: white; padding: 20px; text-align: center; }}
.header h1 {{ margin: 0; font-size: 24px; }}
.content {{ padding: 30px; color: #333333; }}
.content p {{ font-size: 16px; line-height: 1.6; }}
.btn {{ display: inline-block; padding: 14px 24px; margin-top: 20px; background-color: #4CAF50; color: white; text-decoration: none; font-weight: bold; border-radius: 8px; transition: background 0.3s ease; }}
.btn:hover {{ background-color: #45a049; }}
.footer {{ padding: 20px; text-align: center; font-size: 12px; color: #888888; }}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{subject}</h1></div>
<div class="content">
<p>Hola {username} 👋,</p>
<p>¡Enhorabuena! 🎉 Has sido seleccionado como ganador de nuestro sorteo.</p>
<p>Estamos muy emocionados de compartir esta noticia contigo. Para reclamar tu premio, haz clic en el siguiente botón:</p>
<a href="{winner_link}" class="btn">Reclamar premio</a>
<p>Si tienes alguna duda o necesitas asistencia, no dudes en contactarnos.</p>
<p>Gracias por participar y confiar en {company_name} 🍀.</p>
</div>
<div class="footer">© 2025 {company_name}. Todos los derechos reservados.</div>
</div>
</body>
</html>
""",
        },
    },
    "change_password": {
        "subject": "Cambio de contraseña",
        "html_body": """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{subject}</title>
<style>
body {{ font-family: Arial, sans-serif; background-color: #f9fafb; margin: 0; padding: 0; }}
.container {{ max-width: 600px; margin: auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); overflow: hidden; }}
.header {{ background: linear-gradient(90deg, #4CAF50, #2E7D32); color: white; padding: 20px; text-align: center; }}
.header h1 {{ margin: 0; font-size: 24px; }}
.content {{ padding: 30px; color: #333333; }}
.content p {{ font-size: 16px; line-height: 1.6; }}
.btn {{ display: inline-block; padding: 14px 24px; margin-top: 20px; background-color: #4CAF50; color: white; text-decoration: none; font-weight: bold; border-radius: 8px; transition: background 0.3s ease; }}
.btn:hover {{ background-color: #45a049; }}
.footer {{ padding: 20px; text-align: center; font-size: 12px; color: #888888; }}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{subject}</h1></div>
<div class="content">
<p>Hola {username} 👋,</p>
<p>Recibimos una solicitud para cambiar la contraseña de tu cuenta.</p>
<p>Haz clic en el siguiente botón para establecer una nueva contraseña:</p>
<a href="{change_password_link}" class="btn">Cambiar contraseña</a>
<p>Si no solicitaste este cambio, ignora este correo o contacta con soporte.</p>
<p>Gracias por confiar en nosotros 👍.</p>
</div>
<div class="footer">© 2025 {company_name}. Todos los derechos reservados.</div>
</div>
</body>
</html>
""",
    },
    "verification_email": {
        "subject": "Verifica tu correo electrónico",
        "html_body": """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{subject}</title>
<style>
body {{ font-family: Arial, sans-serif; background-color: #f9fafb; margin: 0; padding: 0; }}
.container {{ max-width: 600px; margin: auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); overflow: hidden; }}
.header {{ background: linear-gradient(90deg, #4CAF50, #2E7D32); color: white; padding: 20px; text-align: center; }}
.header h1 {{ margin: 0; font-size: 24px; }}
.content {{ padding: 30px; color: #333333; }}
.content p {{ font-size: 16px; line-height: 1.6; }}
.btn {{ display: inline-block; padding: 14px 24px; margin-top: 20px; background-color: #4CAF50; color: white; text-decoration: none; font-weight: bold; border-radius: 8px; transition: background 0.3s ease; }}
.btn:hover {{ background-color: #45a049; }}
.footer {{ padding: 20px; text-align: center; font-size: 12px; color: #888888; }}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>{subject}</h1></div>
<div class="content">
<p>Hola {username} 👋,</p>
<p>Gracias por registrarte para participar en nuestro sorteo 🎉. Antes de confirmar tu participación, necesitamos que verifiques tu correo electrónico.</p>
<p>Haz clic en el siguiente botón para validar tu dirección y completar tu inscripción:</p>
<a href="{verification_link}" class="btn">Verificar correo</a>
<p>Si no hiciste esta solicitud, ignora este correo.</p>
<p>¡Gracias y mucha suerte 🍀!</p>
</div>
<div class="footer">© 2025 {company_name}. Todos los derechos reservados.</div>
</div>
</body>
</html>
""",
    },
}
