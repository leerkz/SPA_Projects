from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateApiView,
                             LessonDestroyApiView, LessonListApiView,
                             LessonRetrieveApiView, LessonUpdateApiView,
                             SubscriptionCreateApiView, SubscriptionView)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="API проекта",
        default_version="v1",
        description="Автоматически сгенерированная документация API",
        contact=openapi.Contact(email="example@project.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("lesson/", LessonListApiView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveApiView.as_view(), name="lesson_retrieve"),
    path("lesson/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path(
        "lesson/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lessons_delete"
    ),
    path(
        "lesson/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"
    ),
    path("subscribe/", SubscriptionView.as_view(), name="subscribe"),
    path(
        "course/subscription",
        SubscriptionCreateApiView.as_view(),
        name="course_subscription",
    ),
    path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += router.urls
