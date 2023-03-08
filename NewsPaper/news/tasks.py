import datetime

from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import Post


@shared_task
def notify_subscribers_task(post_id: int):
    """Отправляет уведомление подписчиками после создания новости."""
    post = Post.objects.get(pk=post_id)
    html_content = render_to_string('mail.html', {'post': post})

    recipients = []
    for category in post.categories.all():
        for subscriber in category.subscribers.all():
            recipients.append(subscriber.email)

    if len(recipients):
        if post.type == Post.ARTICLE:
            post_type = 'статья'
        else:
            post_type = 'новость'

        msg = EmailMultiAlternatives(
            subject=f'NewsPaper. Новая {post_type} в твоём любимом разделе!',
            body=post.content,
            from_email=f'{settings.EMAIL_HOST_USER}@yandex.ru',
            to=[*list(set(recipients))]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def notify_subscribers_every_week():
    """Отправляет уведомление подписчикам каждую неделю."""
    end = datetime.date.today()
    start = end - datetime.timedelta(days=7)

    for post in Post.objects.filter(dt_created__date__range=(start, end)):
        for category in post.categories.all():
            recipients = []
            for subscriber in category.subscribers.all():
                recipients.append(subscriber.email)

            if len(recipients):
                html_content = render_to_string('mail.html', {'post': post})

                msg = EmailMultiAlternatives(
                    subject=f'NewsPaper. Новая новость в твоём любимом разделе!',
                    body=post.content,
                    from_email=f'{settings.EMAIL_HOST_USER}@yandex.ru',
                    to=[*list(set(recipients))]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
