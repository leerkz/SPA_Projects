from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import LinkValidator


class CourseSerializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.subscription_set.filter(user=user).exists()
        return False


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkValidator(field="link")]


class CourseDetailSerializers(ModelSerializer):
    many_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)
    subscription = serializers.SerializerMethodField()

    def get_subscription(self, course):
        user = self.context["request"].user
        return (
            Subscription.objects.all().filter(user=user).filter(course=course).exists()
        )

    def get_many_lesson(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("title", "description", "many_lessons", "subscription")


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("sign_of_subscription",)
