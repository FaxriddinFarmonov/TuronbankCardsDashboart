from rest_framework.views import APIView
from rest_framework.response import Response

from .models import DashboardStatistics


class DashboardStatisticsAPIView(APIView):

    def get(self, request):

        data = DashboardStatistics.objects.first()

        if not data:
            return Response(
                {"message": "Data not found"},
                status=404
            )

        return Response({
            "total_cards": data.total_cards,

            "active_cards": data.active_cards,
            "active_percent": float(data.active_percent),

            "noactive_cards": data.noactive_cards,
            "noactive_percent": float(data.noactive_percent),

            "virtual_cards": {
                "count": data.virtual_cards_count,
                "percent": float(data.virtual_cards_percent)
            },

            "uzs": {
                "total_balance": str(data.uzs_total_balance),
                "average_balance": str(data.uzs_average_balance),
                "cards_count": data.uzs_cards_count
            },

            "usd": {
                "total_balance": str(data.usd_total_balance),
                "average_balance": str(data.usd_average_balance),
                "cards_count": data.usd_cards_count
            }
        })