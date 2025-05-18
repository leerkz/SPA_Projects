from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_course_update_email(course_id, user_emails):
    from materials.models import \
        Course  # Импорт внутри, чтобы избежать ошибок circular import

    course = Course.objects.get(id=course_id)

    for email in user_emails:
        send_mail(
            subject=f"Обновление курса: {course.title}",
            message="В курсе появились новые материалы!",
            from_email="no-reply@mysite.com",
            recipient_list=[email],
            fail_silently=True,
        )
