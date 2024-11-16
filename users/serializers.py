from rest_framework import serializers
from .models import Payment
from lms.serializers import CourseSerializer, LessonSerializer

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
