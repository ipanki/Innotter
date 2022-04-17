from celery import shared_task
from profiles.send_mails import send_notification
from profiles.models import Page


@shared_task
def send_email(page_id):
    page = Page.objects.get(id=page_id)
    send_notification(page)
    return True
