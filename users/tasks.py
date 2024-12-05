from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def deactivate_inactive_users():
    """
    Деактивирует пользователей, которые не заходили более месяца.
    """
    one_month_ago = now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    # Деактивируем найденных пользователей
    count = inactive_users.update(is_active=False)
    print(f"{count} пользователей были деактивированы.")
