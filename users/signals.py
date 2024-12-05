from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

@receiver(post_migrate)
def create_periodic_task(sender, **kwargs):
    from users.tasks import deactivate_inactive_users
    try:
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )

        PeriodicTask.objects.get_or_create(
            name="Deactivate inactive users",
            defaults={
                "interval": schedule,
                "task": "users.tasks.deactivate_inactive_users",
                "args": json.dumps([]),
            },
        )
        print("Periodic task created or already exists.")
    except Exception as e:
        print(f"Error creating periodic task: {e}")