# views.py
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User, Post, Product
from .serializers import (
    UserRegisterSerializer,
    UserSerializer,
    PostSerializer,
    ProductSerializer
)


# -------------------------
# User Registration
# -------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]  # Anyone can register


# -------------------------
# User ViewSet (Admin actions)
# -------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Only authenticated users can access user data

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def make_admin(self, request, pk=None):
        user = self.get_object()
        user.is_staff = True
        user.save()
        return Response({'status': 'User is now admin'})


# -------------------------
# Post ViewSet (CRUD for posts)
# -------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]  # Must be logged in to write
        return [permissions.AllowAny()]  # Anyone can read posts


# -------------------------
# Product ViewSet (Admin only)
# -------------------------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]  # Only admins can create/update/delete
        return [permissions.AllowAny()]  # Anyone can read products





















# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from .models import Payment
from .serializers import PaymentSerializer
from datetime import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    def post(self, request):
        try:
            price = request.data.get('price')
            amount = int(float(price) * 100)  # Stripe expects cents
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card'],
            )
            return Response({'clientSecret': intent.client_secret})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SavePaymentView(APIView):
    def post(self, request):
        data = request.data
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(date=datetime.now())
            return Response({'paymentResult': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentListView(APIView):
    def get(self, request, email):
        payments = Payment.objects.filter(email=email)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
