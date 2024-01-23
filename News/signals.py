from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory
from NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL


def send_notifications(post, subscribers):
    html_content = render_to_string(
        'new_post_email.html',
        {
            'text': post.preview(),
            'link': f'{SITE_URL}/news/{post.pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=post.title,
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.get_categories()
        subscribers_datas = []
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()

            for subscriber in subscribers:
                subscribers_emails += [subscriber.email]
                subscribers_datas += [{'email': subscriber.email, 'name': subscriber.username}]

        print(subscribers_emails)
        send_notifications(instance, subscribers_emails)


