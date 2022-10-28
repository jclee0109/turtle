from django.urls import path

from profileapp.views import ProfileViewSet

urlpatterns = [
    # Profile
    path('', ProfileViewSet.as_view({'get': 'list'})),
    path('<int:profile_id>', ProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
]