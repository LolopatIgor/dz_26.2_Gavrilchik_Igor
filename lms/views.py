from rest_framework import viewsets,generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.permissions import IsModerator, IsOwner
from .models import Course,Lesson
from .serializers import CourseSerializer, LessonSerializer

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)

