from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
import logging
from django.utils import timezone
from django.conf import settings
from mailing.models import MailingSettings, EmailLog
from mailing.services import sending_mail

logger = logging.getLogger(__name__)


def my_job():
    now = timezone.now()

    for mailing_setting in MailingSettings.objects.filter(status=MailingSettings.objects.filter(status='running')):
        last_attempt = EmailLog.objects.filter(settings=mailing_setting).order_by('-attempt_date').first()

        if last_attempt:
            last_attempt_date = last_attempt.attempt_date
            time_difference = now - last_attempt_date

            if mailing_setting.frequency == 'daily' and time_difference.days >= 1:
                next_send_time = last_attempt_date + timezone.timedelta(days=1, hours=mailing_setting.time.hour,
                                                                        minutes=mailing_setting.time.minute)
                if now >= next_send_time:
                    sending_mail(mailing_setting)
                    logger.info(f"Email sent to clients for MailingSettings {mailing_setting.id}")

            elif mailing_setting.frequency == 'weekly' and time_difference.days >= 7:
                next_send_time = last_attempt_date + timezone.timedelta(weeks=1, hours=mailing_setting.time.hour,
                                                                        minutes=mailing_setting.time.minute)
                if now >= next_send_time:
                    sending_mail(mailing_setting)
                    logger.info(f"Email sent to clients for MailingSettings {mailing_setting.id}")

            elif mailing_setting.frequency == 'monthly' and time_difference.days >= 30:
                next_send_time = last_attempt_date + timezone.timedelta(days=30, hours=mailing_setting.time.hour,
                                                                        minutes=mailing_setting.time.minute)
                if now >= next_send_time:
                    sending_mail(mailing_setting)
                    logger.info(f"Email sent to clients for MailingSettings {mailing_setting.id}")

        else:
            send_time = timezone.datetime(now.year, now.month, now.day, mailing_setting.time.hour,
                                          mailing_setting.time.minute, tzinfo=timezone.get_current_timezone())
            if now >= send_time:
                sending_mail(mailing_setting)
                logger.info(f"Email sent to clients for MailingSettings {mailing_setting.id}")


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
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