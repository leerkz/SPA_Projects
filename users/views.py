from rest_framework import filters, generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials import services
from materials.models import Course
from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]


class CreatePaymentSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        # 1. Создаём продукт в Stripe
        product = services.create_product(
            name=course.name, description=course.description or ""
        )

        # 2. Создаём цену (предположим, course.price есть в центах, иначе умножь)
        price = services.create_price(
            product_id=product.id, amount=int(course.price * 100)
        )

        # 3. Создаём сессию
        session = services.create_checkout_session(
            price_id=price.id,
            success_url="http://localhost:8000/payment/success/",
            cancel_url="http://localhost:8000/payment/cancel/",
        )

        return Response({"checkout_url": session.url})
