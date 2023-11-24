from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class MailingMessage(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема')
    message_content = models.TextField(verbose_name='Содержание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Владелец')
    objects = models.Manager()

    def __str__(self):
        return f'{self.subject}:\n {self.message_content}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Client(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(max_length=100, verbose_name='Почта')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    objects = models.Manager()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='владелец')

    def __str__(self):
        return f'{self.full_name}: {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingSettings(models.Model):
    objects = models.Manager()
    DELIVERY_FREQUENCY_CHOICES = (
        ('daily', 'Ежедневная'),
        ('weekly', 'Еженедельная'),
        ('monthly', 'Ежемесячная'),
    )
    DELIVERY_STATUS_CHOICES = (
        ('completed', 'Завершена'),
        ('created', 'Создана'),
        ('running', 'Запущена'),
    )
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(default=None)
    frequency = models.CharField(max_length=20, choices=DELIVERY_FREQUENCY_CHOICES, default='weekly')
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='created')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE,
                                verbose_name='Сообщение для рассылки', **NULLABLE)
    client = models.ManyToManyField(Client,
                                    verbose_name='Клиент рассылки')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='владелец')
    is_active = models.BooleanField(default=False, verbose_name='Статус активности')

    def __str__(self):
        return f"{self.frequency} рассылка в {self.start_time} {self.client}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('can_set_mailing_activity', 'Can change mailing activity'),
        ]


class EmailLog(models.Model):
    STATUSES = (
        ('STATUS_OK', 'Успешно'),
        ('STATUS_FAILED', 'Ошибка'),
    )
    datetime_attempt = models.DateTimeField(auto_now_add=True, verbose_name='Последняя попытка')
    status = models.CharField(choices=STATUSES, max_length=20, default='STATUS_OK', verbose_name='Статус')
    client = models.ManyToManyField(Client, verbose_name='Клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройки', **NULLABLE)
    objects = models.Manager()

    def __str__(self):
        return f'Логи рассылки - {self.status}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'
