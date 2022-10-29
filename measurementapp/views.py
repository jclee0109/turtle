import datetime
import calendar
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
        data['profile'] = profile_id
        data['average_angle'] = self.get_average_angle(data.get('angles'))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # 평균각도
    def get_average_angle(self, angles):
        angle_sum = 0
        cnt = 0
        for angle in angles:
            angle = float(angle)
            if 0 <= angle <= 90:
                angle_sum += angle
                cnt += 1
        avg = angle_sum // cnt
        return avg

    def retrieve(self, request, measurement_id=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def retrieve_latest(self, request, profile_id=None, *args, **kwargs):
        instance = self.get_queryset().filter(profile_id=profile_id).order_by("-start_datetime").first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, profile_id=None, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(profile_id=profile_id))

        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)

        if (start_date is not None) and (end_date is not None):
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)
            queryset = queryset.filter(start_datetime__gte=start_date, end_datetime__lt=end_date)
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        queryset = queryset.order_by("-start_datetime")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def daily_list(self, request, profile_id=None, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(profile_id=profile_id))
        daily_measurement_dict = {}
        daily_measurement_average_dict = {}
        month = int(request.GET.get("month", datetime.datetime.today().month))
        year = request.GET.get("year", datetime.datetime.today().year)%100
        if year > (datetime.datetime.today().year % 100):
            return Response({"msg": "error"}, status=status.HTTP_400_BAD_REQUEST)
        elif year == (datetime.datetime.today().year%100) and month > datetime.datetime.today().month:
            return Response({"msg": "error"}, status=status.HTTP_400_BAD_REQUEST)

        elif year == (datetime.datetime.today().year%100) and month == datetime.datetime.today().month:
            day = datetime.datetime.today().day
            print("hello")
        else:
            day = calendar.monthrange(year, month)[1]

        for i in range(1, day+1):
            date=f"{year}/{month}/{i}"
            daily_measurement_dict[date]=[]

        for measurement in queryset:
            start_date = measurement.start_datetime.strftime("%y/%m/%d")
            print(start_date)
            if start_date in daily_measurement_dict:
                daily_measurement_dict[start_date].append(measurement.average_angle)

        print(daily_measurement_dict)
        for i in range(1, day+1):
            date = f"{year}/{month}/{i}"
            if len(daily_measurement_dict[date]) == 0:
                daily_measurement_average_dict[date] = 0
            else:
                daily_measurement_average_dict[date] = sum(daily_measurement_dict[date])/len(daily_measurement_dict[date])

        print(daily_measurement_average_dict)
        return Response(list(daily_measurement_average_dict.items()))

    def weekly_list(self, request, profile_id=None, *args, **kwarg):
        pass
    def monthly_list(self, request, profile_id=None, *args, **kwatgs):
        pass