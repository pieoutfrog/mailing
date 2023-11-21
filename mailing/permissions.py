from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from mailing.models import MailingSettings

# Получаем content type для модели Product
content_type = ContentType.objects.get_for_model(MailingSettings)

# Создаем разрешения
Permission.objects.create(
    codename='can_set_mailing_activity',
    name='Can change mailing activity',
    content_type=content_type,
)
