import datetime

from django.db.models.signals import m2m_changed, pre_save, post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

from .models import Post


@receiver(pre_save, sender=Post)
def post_amount_restriction(sender, instance, **kwargs):
    """Не дает создать более трех новостей в сутки."""
    if len(instance.author.posts.filter(dt_created__date=datetime.date.today())) > 2:
        raise PermissionDenied()

@receiver(post_save, sender=User)
def user_greeting(sender, instance, **kwargs):
    html_content = render_to_string('greeting.html', {'user': instance})

    msg = EmailMultiAlternatives(
        subject='NewsPaper приветствует вас!',
        body=html_content,
        from_email=f'{settings.EMAIL_HOST_USER}@yandex.ru',
        to=[instance.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, reverse, **kwargs):
    """Уведомляет подписчика о создании новости с категорией, на которую он подписан."""
    if action == 'post_add' and not reverse:
        html_content = render_to_string('mail.html', {'post': instance})

        recipients = []
        for category in instance.categories.all():
            for subscriber in category.subscribers.all():
                recipients.append(subscriber.email)

        if len(recipients):
            if instance.type == Post.ARTICLE:
                instance_type = 'статья'
            else:
                instance_type = 'новость'

            msg = EmailMultiAlternatives(
                subject=f'NewsPaper. Новая {instance_type} в твоём любимом разделе!',
                body=instance.content,
                from_email=f'{settings.EMAIL_HOST_USER}@yandex.ru',
                to=[*list(set(recipients))]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
