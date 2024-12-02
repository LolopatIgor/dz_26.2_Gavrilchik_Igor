from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from lms.models import Course


@shared_task
def send_course_update_notification(course_id, subscriber_email):
    try:
        course = Course.objects.get(id=course_id)
        subject = f"Обновление курса: {course.name}"
        message = (
            f"Здравствуйте!\n\n"
            f"Курс \"{course.name}\" был обновлен. Проверьте новые материалы!\n\n"
            f"С уважением,\nКоманда обучения."
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [subscriber_email],
            fail_silently=False,
        )
    except Course.DoesNotExist:
        print(f"Курс с ID {course_id} не найден.")
