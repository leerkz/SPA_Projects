import json

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_celery_beat.models import IntervalSchedule, PeriodicTask


@receiver(post_migrate)
def create_periodic_task(sender, **kwargs):
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )

    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name="Deactivate inactive users",
        task="users.tasks.deactivate_inactive_users",
        defaults={"kwargs": json.dumps({})},
    )
