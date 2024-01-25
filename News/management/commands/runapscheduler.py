import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives

from NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL, TIME_ZONE

from ...models import User, Post

logger = logging.getLogger(__name__)


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


def send_weekly_mail():
    dict_for_mailing = get_subscribers_with_posts()
    # print('send', dict_for_mailing)

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


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = 'Runs apscheduler.'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_mail,
            trigger=CronTrigger(day_of_week='thu', hour='14', minute='26'),
            id="send_weekly_mail",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
