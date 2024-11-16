from django.db import models
from django.contrib.auth.models import AbstractUser
from lms.models import Course, Lesson

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Наличные'),
        ('bank_transfer', 'Перевод на счет'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"{self.user} paid {self.amount} on {self.payment_date}"
