from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserViewSet, PostViewSet, ProductViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreatePaymentIntentView, PaymentListView, SavePaymentView

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('posts', PostViewSet)
router.register('products', ProductViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('payments/', SavePaymentView.as_view(), name='save-payment'),
    path('payments/<str:email>/', PaymentListView.as_view(), name='get-payments'),


    path('', include(router.urls)),
]
