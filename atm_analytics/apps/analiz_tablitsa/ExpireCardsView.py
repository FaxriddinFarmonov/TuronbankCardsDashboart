
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
import requests
from django.core.management.base import BaseCommand
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ExpireCardsReport, ExpireCardsItem





def save_expire_cards(data: dict):

    report = ExpireCardsReport.objects.create(
        total_cards=data["total_cards"]
    )

    mapping = [
        ("expire_in_30_days", "0-30 days"),
        ("expire_in_30_60_days", "30-60 days"),
        ("expire_in_60_90_days", "60-90 days"),
    ]

    items = []

    for key, label in mapping:
        items.append(
            ExpireCardsItem(
                report=report,
                period=label,
                count=data[key]["count"],
                percent=data[key]["percent"]
            )
        )

    ExpireCardsItem.objects.bulk_create(items)

    return report



class SyncExpireCardsAPIView(APIView):

    def post(self, request):

        data = requests.get(
            "http://127.0.0.1:8000/expire-cards/"
        ).json()

        report = save_expire_cards(data)

        return Response({
            "message": "expire cards synced successfully",
            "report_id": report.id
        })




class ExpireCardsAPIView(APIView):

    def get(self, request):

        report = ExpireCardsReport.objects.prefetch_related(
            "expire_statistics"
        ).first()

        if not report:
            return Response({"message": "no data"}, status=404)

        return Response({
            "total_cards": report.total_cards,

            "statistics": [
                {
                    "period": i.period,
                    "count": i.count,
                    "percent": float(i.percent)
                }
                for i in report.expire_statistics.all()
            ]
        })


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        data = requests.get(
            "http://127.0.0.1:8000/expire-cards/"
        ).json()

        save_expire_cards(data)

        self.stdout.write(
            self.style.SUCCESS("Expire cards synced successfully")
        )


def sync_expire_cards_cron():

    try:


        factory = APIRequestFactory()

        request = factory.post(
            "/expire-cards/sync/"
        )

        response = SyncExpireCardsAPIView.as_view()(request)

        print("SUCCESS:", response.data)

    except Exception as e:

        print("ERROR:", str(e))