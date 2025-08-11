from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
import json


# Create your views here.
@csrf_exempt
@require_POST
def send_mail_view(request):
    data = json.loads(request.body)
    name = data.get("name", "")
    mail = data.get("mail", "")
    message = data.get("message", "")
    subject = f"Casa do Santo/Formulario Contacto"
    mail_body = f"""
        El/la señor/a {name} ha escrito un correo: \n
        {message}\n
        Por favor respondedle lo antes posible al correo {mail}
    """
    recipient_list = ["casadosantocoira@gmail.com"]

    try:
        send_mail(
            subject,
            mail_body,
            "casadosantocoira@gmail.com",  # From email (configured in settings)
            recipient_list,  # To email(s)
            fail_silently=False,  # Raise errors if sending fails
            # Optional: To make 'Reply-To' work correctly in email clients
            # headers={'Reply-To': from_email}
        )
    except Exception as e:
        print("error:", e)
        return JsonResponse({"message": str(e)})
    # --- Email Content ---
    # Email sent successfully
    return JsonResponse({"message": "Email sent successfully!"})
