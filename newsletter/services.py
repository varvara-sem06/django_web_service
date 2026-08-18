from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import MailingAttempt


def send_mailing(mailing):

    if mailing.is_disabled:
        raise ValueError("Рассылка отключена менеджером.")

    now = timezone.now()

    if not (mailing.start_time <= now <= mailing.end_time):
        raise ValueError("Рассылка сейчас недоступна.")

    recipients = mailing.recipients.all()
    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )

            MailingAttempt.objects.create(
                mailing=mailing,
                status=MailingAttempt.STATUS_SUCCESS,
                server_response="Сообщение успешно отправлено.",
            )

        except Exception as error:
            MailingAttempt.objects.create(
                mailing=mailing,
                status=MailingAttempt.STATUS_FAILED,
                server_response=str(error),
            )
