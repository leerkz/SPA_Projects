from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (CreatePaymentSessionView, PaymentsViewSet,
                         UserCreateAPIView)

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", PaymentsViewSet)

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
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "token/refresh",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "register/",
        UserCreateAPIView.as_view(permission_classes=(AllowAny,)),
        name="register",
    ),
    re_path(
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
    path(
        "api/payment/",
        CreatePaymentSessionView.as_view(),
        name="create-payment-session",
    ),
]
