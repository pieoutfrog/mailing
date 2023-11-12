from datetime import datetime, timedelta

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from .models import MailingSettings, EmailLog


def add_jobs(scheduler):
    for mailing_setting in MailingSettings.objects.filter(status='running'):
        add_job(scheduler, mailing_setting)


def add_job(scheduler, mailing_setting, form=None):
    # задать вопрос про интервал и как использовать уже имеющиеся настройки рассылки в часах, днях и т.д.
    for mailing_setting in MailingSettings.objects.filter(status='running'):
        hours, minutes = mailing_setting.start_time.hour, mailing_setting.start_time.minute
        if mailing_setting.frequency == 'daily':
            # Запуск задачи ежедневно в указанное время
            trigger_time = CronTrigger(hour=mailing_setting.start_time.hour, minute=mailing_setting.start_time.minute)
            scheduler.add_job(
                sending_mail,
                trigger=trigger_time,
                id=str(mailing_setting.pk),
                args=(mailing_setting,)
            )
            EmailLog.objects.create(
                client=form.cleaned_data['client'],
                status=form.cleaned_data['status'],
                settings=mailing_setting
            )

        elif mailing_setting.frequency == 'weekly':
            # Запуск задачи каждую неделю в указанный день и время
            trigger_time = CronTrigger(day_of_week=mailing_setting.start_time.weekday(),
                                       hour=mailing_setting.start_time.hour, minute=mailing_setting.start_time.minute)
            scheduler.add_job(
                sending_mail,
                trigger=trigger_time,
                id=str(mailing_setting.pk),
                args=(mailing_setting,)
            )
            EmailLog.objects.create(
                client=form.cleaned_data['client'],
                status=form.cleaned_data['status'],
                settings=mailing_setting
            )

        elif mailing_setting.frequency == 'monthly':
            # Запуск задачи каждый месяц в указанный день и время
            trigger_time = CronTrigger(day=mailing_setting.start_time.day, hour=mailing_setting.start_time.hour,
                                       minute=mailing_setting.start_time.minute)
            scheduler.add_job(
                sending_mail,
                trigger=trigger_time,
                id=str(mailing_setting.pk),
                args=(mailing_setting,)
            )
            EmailLog.objects.create(
                client=form.cleaned_data['client'],
                status=form.cleaned_data['status'],
                settings=mailing_setting
            )


def sending_mail(mailing_setting):
    clients = mailing_setting.client.all()
    email_list = [client.email for client in clients]
    message = mailing_setting.message
    send_mail(
        subject=message.subject,
        message=message.message_content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email_list,
        fail_silently=False,
    )
