import datetime

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models import QuerySet
from django.template.loader import render_to_string

from .models import Post
from NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL


@shared_task
def send_email_about_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.get_categories()
    subscribers_emails = []

    for cat in categories:
        subscribers = cat.subscribers.all()

        for subscriber in subscribers:
            subscribers_emails += [subscriber.email]

    send_notifications(post, subscribers_emails)


def send_notifications(post, subscribers):
    html_content = render_to_string(
        'account/email/new_post_email.html',
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


@shared_task
def send_weekly_mail():
    dict_for_mailing = get_subscribers_with_posts()

    for user, posts in dict_for_mailing.items():
        html_content = render_to_string(
            'account/email/weekly_email.html',
            {
                'SITE_URL': SITE_URL,
                'posts': posts,
            }
        )

        msg = EmailMultiAlternatives(
            subject="Еженедельная рассылка",
            from_email=DEFAULT_FROM_EMAIL,
            to=[user]
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


def get_subscribers_with_posts() -> dict[User.email: QuerySet]:
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    subs_posts_dict = dict()
    for user in User.objects.all():
        posts = QuerySet(model=Post).none()
        if user.categories.all():
            for cat in user.categories.all():
                posts = posts.union(cat.posts_categories.filter(add_date__gte=last_week))
            subs_posts_dict[user.email] = posts.iterator()
    return subs_posts_dict
