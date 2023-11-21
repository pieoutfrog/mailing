from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from users.models import User

# Получаем content type для модели Product
content_type = ContentType.objects.get_for_model(User)
Permission.objects.create(
    codename='can_set_user_blocked',
    name='Can block user',
    content_type=content_type,
)
Permission.objects.create(
    codename='can_view_users',
    name='Can view users',
    content_type=content_type,
)
