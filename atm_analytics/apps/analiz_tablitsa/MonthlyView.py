
import requests
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MonthlyIssuedCardsReport, MonthlyIssuedCardsItem


def save_monthly_issued_cards(data: dict):

    report = MonthlyIssuedCardsReport.objects.create(
        year=data["year"]
    )

    items = []

    for month, value in data["monthly_cards"].items():
        items.append(
            MonthlyIssuedCardsItem(
                report=report,
                month=month,
                cards_count=value
            )
        )

    MonthlyIssuedCardsItem.objects.bulk_create(items)

    return report


class SyncMonthlyIssuedCardsAPIView(APIView):

    def post(self, request):

        data = requests.get(
            "http://127.0.0.1:8000/monthly-issued-cards/"
        ).json()

        report = save_monthly_issued_cards(data)

        return Response({
            "message": "monthly cards synced successfully",
            "report_id": report.id
        })


class MonthlyIssuedCardsAPIView(APIView):

    def get(self, request):

        report = MonthlyIssuedCardsReport.objects.prefetch_related(
            "monthly_cards"
        ).first()

        if not report:
            return Response({"message": "no data"}, status=404)

        return Response({
            "year": report.year,

            "monthly_cards": {
                item.month: item.cards_count
                for item in report.monthly_cards.all()
            }
        })


def sync_monthly_issued_cards_cron():

    try:


        factory = APIRequestFactory()

        request = factory.post(
            "/monthly-issued-cards/sync/"
        )

        response = SyncMonthlyIssuedCardsAPIView.as_view()(request)

        print("SUCCESS:", response.data)

    except Exception as e:
        print("ERROR:", str(e))