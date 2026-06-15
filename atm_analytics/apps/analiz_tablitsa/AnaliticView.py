from rest_framework.test import APIRequestFactory
from .models import AnalyticsReport, CardStatusItem, ResidentItem, ClientTypeItem

def save_analytics(data: dict):

    report = AnalyticsReport.objects.create(
        total_cards=data["total_cards"]
    )

    # CARD STATUS
    CardStatusItem.objects.bulk_create([
        CardStatusItem(
            report=report,
            card_status=i["card_status"],
            cards_count=i["cards_count"],
            percentage=i["percentage"]
        )
        for i in data["card_status_statistics"]
    ])

    # RESIDENT
    ResidentItem.objects.bulk_create([
        ResidentItem(
            report=report,
            resident_status=i["resident_status"],
            title=i["title"],
            cards_count=i["cards_count"],
            percentage=i["percentage"]
        )
        for i in data["resident_statistics"]
    ])

    # CLIENT TYPE
    ClientTypeItem.objects.bulk_create([
        ClientTypeItem(
            report=report,
            client_type=i["client_type"],
            cards_count=i["cards_count"],
            percentage=i["percentage"]
        )
        for i in data["client_type_statistics"]
    ])

    return report


import requests
from rest_framework.views import APIView
from rest_framework.response import Response



class SyncAnalyticsAPIView(APIView):

    def post(self, request):

        data = requests.get(
            "http://127.0.0.1:8000/analytics/"
        ).json()

        report = save_analytics(data)

        return Response({
            "message": "synced successfully",
            "report_id": report.id
        })


class AnalyticsAPIView(APIView):

    def get(self, request):

        report = AnalyticsReport.objects.prefetch_related(
            "card_status_statistics",
            "resident_statistics",
            "client_type_statistics"
        ).first()

        if not report:
            return Response({"message": "no data"}, status=404)

        return Response({
            "total_cards": report.total_cards,

            "card_status_statistics": [
                {
                    "card_status": i.card_status,
                    "cards_count": i.cards_count,
                    "percentage": float(i.percentage)
                }
                for i in report.card_status_statistics.all()
            ],

            "resident_statistics": [
                {
                    "resident_status": i.resident_status,
                    "title": i.title,
                    "cards_count": i.cards_count,
                    "percentage": float(i.percentage)
                }
                for i in report.resident_statistics.all()
            ],

            "client_type_statistics": [
                {
                    "client_type": i.client_type,
                    "cards_count": i.cards_count,
                    "percentage": float(i.percentage)
                }
                for i in report.client_type_statistics.all()
            ]
        })



def sync_analytics_cron():

    try:



        factory = APIRequestFactory()

        request = factory.post(
            "/analytics/sync/"
        )

        response = SyncAnalyticsAPIView.as_view()(request)

        print("SUCCESS:", response.data)

    except Exception as e:

        print("ERROR:", str(e))
