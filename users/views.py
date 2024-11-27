from rest_framework.response import Response
from rest_framework import viewsets, filters, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from lms.models import Course
from lms.services import create_stripe_product, create_stripe_price, create_stripe_session
from .models import Payment, User
from .serializers import PaymentSerializer, UserRegistrationSerializer, UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("POST request received")
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        amount = int(course.price * 100)  # Цена в центах
        currency = 'usd'

        # Создаем продукт в Stripe
        stripe_product = create_stripe_product(course.name)

        # Создаем цену в Stripe
        stripe_price = create_stripe_price(amount, currency, stripe_product['id'])

        # Создаем сессию оплаты в Stripe
        success_url = 'http://localhost:8000/success/'
        cancel_url = 'http://localhost:8000/cancel/'
        session = create_stripe_session(stripe_price['id'], success_url, cancel_url)

        # Создаем запись платежа
        payment = Payment.objects.create(
            user=user,
            paid_course=course,
            amount=course.price,
            payment_method='card',
            stripe_product_id=stripe_product['id'],
            stripe_price_id=stripe_price['id'],
            stripe_session_id=session['id'],
            payment_url=session['url']
        )

        serializer = PaymentSerializer(payment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
