from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from measurementapp.models import Measurement
from measurementapp.serializers import MeasurementSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'measurement_id'

    def create(self, request, profile_id=None, *args, **kwargs):
        data=request.data.copy()
        print(data)
        data['profile'] = profile_id
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, measurement_id=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def retrieve_latest(self, request, profile_id=None, *args, **kwargs):
        instance = self.get_queryset().filter(profile_id=profile_id).order_by("-start_datetime").first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, profile_id=None, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(profile_id=profile_id).order_by("-start_datetime"))

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)