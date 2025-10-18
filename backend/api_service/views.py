from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from django.core.mail import send_mail
import json

from .models import EmailTemplate


# Create your views here.
@csrf_exempt
@require_POST
def send_mail_view(request):
    try:

        # recuperate data from json
        data = json.loads(request.body)
        name = data.get("name", "")
        mail = data.get("mail", "")
        message = data.get("message", "")
        language = data.get("language", "")

        # recuperate mail template
        try:
            template = EmailTemplate.objects.get(slug="mail_contact")
        except EmailTemplate.DoesNotExist:
            # Return an error if the template isn't found
            return JsonResponse(
                {"error": "The required email template was not found."}, status=404
            )

        subject = template.excerpt
        mail_body = template.content
        mail_body = mail_body.replace("{name}", name)
        mail_body = mail_body.replace("{message}", message)
        mail_body = mail_body.replace("{mail}", mail)
        mail_body = mail_body.replace("{language}", language)

        recipient_list = ["casadosantocoira@gmail.com"]

        # send mail
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
    except Exception as e:
        # Email sent failed
        return JsonResponse({"message": "Email sent failed!"})


@csrf_exempt
@require_POST
def send_reservation_mail_view(request):
    try:
        # recuperate data from json
        data = json.loads(request.body)
        name = data.get("name", "")
        mail = data.get("mail", "")
        message = data.get("message", "")
        check_in = data.get("checkInDate", "")
        check_out = data.get("checkOutDate", "")
        n_adults = data.get("n_adults", "")
        n_childs = data.get("n_childs", "")
        language = data.get("language", "")

        # recuperate mail template
        try:
            template = EmailTemplate.objects.get(slug="mail_reservation_data")
        except EmailTemplate.DoesNotExist:
            # Return an error if the template isn't found
            return JsonResponse(
                {"error": "The required email template was not found."}, status=404
            )

        subject = template.excerpt
        mail_body = template.content
        mail_body = mail_body.replace("{name}", name)
        mail_body = mail_body.replace("{message}", message)
        mail_body = mail_body.replace("{mail}", mail)
        mail_body = mail_body.replace("{language}", language)
        mail_body = mail_body.replace("{checkInDate}", check_in)
        mail_body = mail_body.replace("{checkOutDate}", check_out)
        mail_body = mail_body.replace("{n_adults}", str(n_adults))
        mail_body = mail_body.replace("{n_childs}", str(n_childs))

        recipient_list = ["casadosantocoira@gmail.com"]

        # send mail
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

        # recuperate mail template ANSWER
        try:
            template = EmailTemplate.objects.get(slug="mail_reservation_answer")
        except EmailTemplate.DoesNotExist:
            # Return an error if the template isn't found
            return JsonResponse(
                {"error": "The required email template was not found."}, status=404
            )

        try:
            subject = template.excerpt
            mail_body = template.content
            recipient_list = [mail]
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
    except Exception as e:
        # Email sent failed
        return JsonResponse({"message": "Email sent failed!"})


def send_reservation_confimation_mail(request, mail, token, total_price, check_in_date, check_out_date):
    try:
        template = EmailTemplate.objects.get(slug="mail_reservation_url")
        subject = template.excerpt
        mail_body = template.content
        mail_body = mail_body.replace("{uuid}", token)
        mail_body = mail_body.replace("{total_price}", total_price)
        mail_body = mail_body.replace("{check_in_date}", check_in_date)
        mail_body = mail_body.replace("{check_out_date}", check_out_date)
        recipient_list = [mail]
        send_mail(
            subject,
            mail_body,
            "casadosantocoira@gmail.com",  # From email (configured in settings)
            recipient_list,  # To email(s)
            fail_silently=False,  # Raise errors if sending fails
            html_message=mail_body,
            # Optional: To make 'Reply-To' work correctly in email clients
            # headers={'Reply-To': from_email}
        )

    except EmailTemplate.DoesNotExist:
        # Return an error if the template isn't found
        return JsonResponse(
            {"error": "The required email template was not found."}, status=404
        )
