import dj_rest_auth
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accountapp.views import UserViewSet

urlpatterns = [
    # Django Rest Auth
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration', include('dj_rest_auth.registration.urls')),

    path('<int:id>', UserViewSet.as_view({'get': 'retrieve'})),
    path('me', UserViewSet.as_view({'get': 'retrieve_sef', 'delete': 'destroy'}))
]