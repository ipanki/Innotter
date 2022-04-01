from django.core.mail import send_mail


def send_notification(page):

    for user in page.followers.all():
        send_mail(
            'New post',
            f"{user} Posted new post",
            'daniil.panko@gmail.com',
            [f'{user.email}'],
            fail_silently=False, )
