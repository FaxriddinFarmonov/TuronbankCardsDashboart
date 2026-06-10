from rest_framework.views import APIView
from rest_framework.response import Response

from .models import HeadOfficeActivity


class HeadOfficeActivityAPIView(APIView):

    def get(self, request):

        report = HeadOfficeActivity.objects.prefetch_related(
            "head_offices"
        ).first()

        if not report:
            return Response({"message": "No data"}, status=404)

        return Response({
            "active_days": report.active_days,
            "total_active_cards": report.total_active_cards,

            "head_offices": [
                {
                    "head_office": item.head_office,
                    "active_cards": item.active_cards,
                    "percentage": float(item.percentage)
                }
                for item in report.head_offices.all()
            ]
        })