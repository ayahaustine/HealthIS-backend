from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView, ProfileView

urlpatterns = [
    path('auth/', include([
        path('register/', RegisterView.as_view(), name='auth_register'),
        path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('logout/', LogoutView.as_view(), name='auth_logout'),
        path('me/', ProfileView.as_view(), name='user_profile')
    ])),
]