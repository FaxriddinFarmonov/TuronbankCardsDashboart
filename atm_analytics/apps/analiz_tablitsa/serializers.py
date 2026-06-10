from rest_framework import serializers
from .models import DashboardStatistics


class DashboardStatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DashboardStatistics
        fields = "__all__"