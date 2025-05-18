from datetime import timedelta


from django.utils import timezone
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializer import (CourseSerializer, LessonSerializer,
                                  SubscriptionSerializer)
from users.permissions import ItsModer, ItsOwner


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})


# Create your views here.
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_update(self, serializer, send_course_update_email=None):
        instance = serializer.save()

        # Проверка: обновлялся ли курс за последние 4 часа
        if timezone.now() - instance.updated_at > timedelta(hours=4):
            # Получаем подписчиков
            subscribers = Subscription.objects.filter(course=instance)
            emails = [sub.user.email for sub in subscribers if sub.user.email]

            # Вызываем таску Celery
            send_course_update_email.delay(instance.id, emails)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~ItsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (ItsModer | ItsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (ItsModer | ItsOwner,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~ItsModer, IsAuthenticated)


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (ItsModer | ItsOwner, IsAuthenticated)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (ItsModer | ItsOwner, IsAuthenticated)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (ItsModer | ItsOwner, IsAuthenticated)


class SubscriptionCreateApiView(CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(
                user=user, course=course_item, sign_of_subscription=True
            )
            message = "подписка добавлена"
        return Response({"message": message})
