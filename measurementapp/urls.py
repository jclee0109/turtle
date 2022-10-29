from django.urls import path

from measurementapp.views import MeasurementViewSet
from profileapp.views import ProfileViewSet

urlpatterns = [
    # Profile
    path('profiles/<int:profile_id>/measurements', MeasurementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('profiles/<int:profile_id>/measurements/latest', MeasurementViewSet.as_view({'get': 'retrieve_latest'})),
    path('profiles/<int:profile_id>/measurements/<int:measurements_id>', MeasurementViewSet.as_view({'get': 'retrieve'})),
    path('profiles/<int:profile_id>/measurements/daily', MeasurementViewSet.as_view({'get': 'daily_list'})),
]