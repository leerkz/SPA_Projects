from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.com")
        self.course = Course.objects.create(
            name="Python course", description="Python course jun", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Python lesson",
            description="Python course",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"name": "Python"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Python")

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "picture": None,
                    "description": self.lesson.description,
                    "link": "",
                    "owner": self.user.pk,
                    "course": self.course.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.com")
        self.course = Course.objects.create(
            name="Python course", description="Python course jun", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Python lesson",
            description="Python course decorators",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse("materials:course_subscription")
        data = {
            "user": self.user.pk,
            "course": self.course.pk,
            "lesson": self.lesson.pk,
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": "подписка добавлена"})

    def test_subscription_delete(self):
        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            lesson=self.lesson,
            sign_of_subscription=True,
        )
        url = reverse("materials:course_subscription")
        data = {
            "user": self.user.pk,
            "course": self.course.pk,
            "lesson": self.lesson.pk,
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": "подписка удалена"})
