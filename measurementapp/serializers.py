import datetime

from rest_framework import serializers

from measurementapp.models import Measurement
import math

class MeasurementSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    average_angle = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    _average_angle = serializers.FloatField(read_only=True)

    def get_day(self, obj):
        return datetime.datetime.weekday(obj.start_datetime)

    # 사용한시간 (분단위, 초는 그냥 버림)
    def get_duration(self, obj):
        return math.ceil((obj.end_datetime - obj.start_datetime).total_seconds()/60)

    def get_weight(self, obj):
        return 0.364*(obj.base_angle + 15 - self._average_angle) + 5.7788

    # 평균각도
    def get_average_angle(self, obj):
        angles = obj.angles
        angle_sum = 0
        cnt = 0
        for angle in angles:
            if 0 <= angle <= 90:
                angle_sum += angle
                cnt += 1
        avg = angle_sum // cnt
        self._average_angle = avg
        return avg

    class Meta:
        model = Measurement
        fields = '__all__'
