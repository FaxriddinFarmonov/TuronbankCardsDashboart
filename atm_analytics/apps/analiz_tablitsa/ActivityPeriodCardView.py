
import requests

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ActivityPeriodReport, ActivityPeriodItem


def save_activity_period(data: dict):

    report = ActivityPeriodReport.objects.create(
        today=data["today"],
        total_cards=data["total_cards"]
    )

    items = [
        ActivityPeriodItem(
            report=report,
            period=i["period"],
            cards_count=i["cards_count"],
            percentage=i["percentage"]
        )
        for i in data["statistics"]
    ]

    ActivityPeriodItem.objects.bulk_create(items)

    return report



class SyncActivityPeriodAPIView(APIView):

    def post(self, request):

        data = requests.get(
            "http://127.0.0.1:8000/activity-period-statistics/"
        ).json()

        report = save_activity_period(data)

        return Response({
            "message": "synced successfully",
            "report_id": report.id
        })



class ActivityPeriodAPIView(APIView):

    def get(self, request):

        report = ActivityPeriodReport.objects.prefetch_related(
            "statistics"
        ).first()

        if not report:
            return Response({"message": "no data"}, status=404)

        return Response({
            "today": report.today,
            "total_cards": report.total_cards,

            "statistics": [
                {
                    "period": i.period,
                    "cards_count": i.cards_count,
                    "percentage": float(i.percentage)
                }
                for i in report.statistics.all()
            ]
        })

