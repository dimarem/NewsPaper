import datetime

from django.db.models.signals import m2m_changed, pre_save, post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

from .models import Post
from .tasks import notify_subscribers_task


@receiver(pre_save, sender=Post)
def post_amount_restriction(sender, instance, **kwargs):
    """Не дает создать более трех новостей в сутки."""
    if len(instance.author.posts.filter(dt_created__date=datetime.date.today())) > 2:
        raise PermissionDenied()


@receiver(post_save, sender=User)
def user_greeting(sender, instance, **kwargs):
    """Отправляет приветственное письмо после регистрации пользователя."""
    html_content = render_to_string('greeting.html', {'user': instance})

    msg = EmailMultiAlternatives(
        subject='NewsPaper приветствует вас!',
        body=html_content,
        from_email=f'{settings.EMAIL_HOST_USER}@yandex.ru',
        to=[instance.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# @receiver(m2m_changed, sender=Post.categories.through)
# def notify_subscribers(sender, instance, action, reverse, **kwargs):
#     """Уведомляет подписчика о создании новости с категорией, на которую он подписан."""
#     if action == 'post_add' and not reverse:
#         notify_subscribers_task.delay(instance.id)
