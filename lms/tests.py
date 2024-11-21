from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()

class LMSAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')

        # Создаем курс
        self.course = Course.objects.create(name='Тестовый курс', description='Описание курса', owner=self.user1)

        # Создаем урок
        self.lesson = Lesson.objects.create(
            course=self.course,
            name='Тестовый урок',
            description='Описание урока',
            video_link='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            owner=self.user1
        )

    def test_lesson_crud(self):
        # Аутентифицируемся под user1
        self.client.force_authenticate(user=self.user1)

        # Создаем урок
        url = reverse('lms:lesson-list')
        data = {
            'course': self.course.id,
            'name': 'Новый урок',
            'description': 'Описание нового урока',
            'video_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        lesson_id = response.data['id']

        # Получаем список уроков
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Обновляем урок
        url_detail = reverse('lms:lesson-detail', args=[lesson_id])
        data_update = {
            'course': self.course.id,  # Обязательно указываем поле course
            'name': 'Обновленное название урока',
            'description': 'Обновленное описание',
            'video_link': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        }
        response = self.client.put(url_detail, data_update, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Обновленное название урока')

        # Удаляем урок
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscription(self):
        # Аутентифицируемся под user1
        self.client.force_authenticate(user=self.user2)

        # Подписываемся на курс
        url = reverse('lms:subscribe')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

        # Проверяем, что подписка существует
        self.assertTrue(Subscription.objects.filter(user=self.user2, course=self.course).exists())

        # Получаем информацию о курсе и проверяем поле is_subscribed
        url_course_detail = reverse('lms:course-detail', kwargs={'pk': self.course.id})
        response = self.client.get(url_course_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])

        # Отписываемся от курса
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')

        # Проверяем, что подписка удалена
        self.assertFalse(Subscription.objects.filter(user=self.user1, course=self.course).exists())

    def test_lesson_validation(self):
        self.client.force_authenticate(user=self.user1)

        url = reverse('lms:lesson-list')  # Include the namespace 'lms'
        data = {
            'course': self.course.id,
            'name': 'Урок с неправильной ссылкой',
            'description': 'Описание урока',
            'video_link': 'https://www.vimeo.com/123456',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_link', response.data)
        self.assertEqual(response.data['video_link'][0], 'Ссылка должна вести на youtube.com')
