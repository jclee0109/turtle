import datetime

from rest_framework import serializers

from measurementapp.models import Measurement
import math

class MeasurementSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()

    def get_day(self, obj):
        return datetime.datetime.weekday(obj.start_datetime)

    # 사용한시간 (분단위, 초는 그냥 버림)
    def get_duration(self, obj):
        return math.ceil((obj.end_datetime - obj.start_datetime).total_seconds()/60)

    # 부하계산
    def get_weight(self, obj):
        return 0.364*(obj.base_angle + 15 - obj.average_angle) + 5.7788

    class Meta:
        model = Measurement
        fields = '__all__'
