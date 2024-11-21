from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, SubscriptionAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

app_name = 'lms'

urlpatterns = [
    path('', include(router.urls)),
    path('subscribe/', SubscriptionAPIView.as_view(), name='subscribe'),
]
