from rest_framework.response import Response

import requests
from rest_framework.views import APIView
from rest_framework.test import APIRequestFactory

from .models import (
    BalanceStatisticsReport,
    BalanceStatisticsItem,
)




def save_balance_statistics(data: dict):

    report = BalanceStatisticsReport.objects.create(
        currency=data["currency"],
        total_cards=data["total_cards"]
    )

    items = [
        BalanceStatisticsItem(
            report=report,
            category=i["category"],
            cards_count=i["cards_count"],
            percentage=i["percentage"]
        )
        for i in data["statistics"]
    ]

    BalanceStatisticsItem.objects.bulk_create(items)

    return report

class SyncBalanceStatisticsAPIView(APIView):

    def post(self, request):

        data = requests.get(
            "http://127.0.0.1:8000/balance-statistics/"
        ).json()

        report = save_balance_statistics(data)

        return Response({
            "message": "synced successfully",
            "report_id": report.id
        })


class BalanceStatisticsAPIView(APIView):

    def get(self, request):

        report = BalanceStatisticsReport.objects.prefetch_related(
            "statistics"
        ).first()

        if not report:
            return Response({"message": "no data"}, status=404)

        return Response({
            "currency": report.currency,
            "total_cards": report.total_cards,

            "statistics": [
                {
                    "category": i.category,
                    "cards_count": i.cards_count,
                    "percentage": float(i.percentage)
                }
                for i in report.statistics.all()
            ]
        })



def sync_balance_statistics_cron():

    try:

        factory = APIRequestFactory()

        request = factory.post(
            "/balance-statistics/sync/"
        )

        response = SyncBalanceStatisticsAPIView.as_view()(request)

        print("SUCCESS:", response.data)

    except Exception as e:

        print("ERROR:", str(e))