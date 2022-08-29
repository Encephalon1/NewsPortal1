from celery import shared_task
import datetime
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from .email_recipients_subscribers import email_recipients_subscribers


@shared_task
def send_mail():
    html_content = render_to_string('mail_for_subscriber.html')

    msg = EmailMultiAlternatives(
        subject=f'{Post.objects.latest("id").title}',
        body=Post.objects.latest('id').post_text[:50],
        from_email='Encephalon135@yandex.ru',
        to=email_recipients_subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def week_mail():
    html_content = render_to_string('mail_for_subscriber.html')
    date_of_posts = datetime.date.today() - timedelta(days=7)

    msg = EmailMultiAlternatives(
        subject='Новые статьи в выбранной категории',
        # Выбираем новости за каждый из дней прошедшей недели
        body=Post.objects.filter(date_and_time_of_creation_post__in=
                                 [datetime.date.today() - timedelta(days=7),
                                  datetime.date.today() - timedelta(days=6),
                                  datetime.date.today() - timedelta(days=5),
                                  datetime.date.today() - timedelta(days=4),
                                  datetime.date.today() - timedelta(days=3),
                                  datetime.date.today() - timedelta(days=2),
                                  datetime.date.today() - timedelta(days=1)]).post_text[:50],
        from_email='Encephalon135@yandex.ru',
        to=email_recipients_subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
