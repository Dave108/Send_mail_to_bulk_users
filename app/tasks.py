from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True)
def mailing_func_user(self, username, password):
    # operation to perform
    print(password, username, "inside the tasks----------------- using celery beat")
    user = get_user_model().objects.get(username=username)
    subject = "Congrats for Signing-Up"
    message = "Thankyou {0} for signing up with us, here is your Password \"{1}\".".format(username, password)
    to_email = user.email
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )

    return "SUCCESS mail sent-to-new users"
