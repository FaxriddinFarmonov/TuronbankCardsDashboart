import requests
from django.core.management import BaseCommand
from rest_framework.test import APIRequestFactory



from rest_framework.views import APIView
from rest_framework.response import Response

from .models import CardTypeStatistics, CardTypeItem


def save_card_type_statistics(data: dict):

    report = CardTypeStatistics.objects.create(
        total_cards=data["total_cards"]
    )

    items = []

    for item in data["card_types"]:
        items.append(
            CardTypeItem(
                report=report,
                card_type=item["card_type"],
                cards_count=item["cards_count"],
                percentage=item["percentage"],
                systems=item.get("systems", [])
            )
        )

    CardTypeItem.objects.bulk_create(items)

    return report



class SyncCardTypeStatisticsAPIView(APIView):

    def post(self, request):

        data = requests.get(
            "http://127.0.0.1:8000/card-type-statistics/"
        ).json()

        report = save_card_type_statistics(data)

        return Response({
            "message": "synced successfully",
            "report_id": report.id
        })




class CardTypeStatisticsAPIView(APIView):

    def get(self, request):

        report = CardTypeStatistics.objects.prefetch_related(
            "card_types"
        ).first()

        if not report:
            return Response({"message": "No data"}, status=404)

        return Response({
            "total_cards": report.total_cards,

            "card_types": [
                {
                    "card_type": item.card_type,
                    "cards_count": item.cards_count,
                    "percentage": float(item.percentage),
                    "systems": item.systems
                }
                for item in report.card_types.all()
            ]
        })






class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        data = requests.get(
            "http://127.0.0.1:8000/card-type-statistics/"
        ).json()

        save_card_type_statistics(data)

        self.stdout.write(
            self.style.SUCCESS("Card type synced successfully")
        )


def sync_card_type_statistics_cron():

    try:

        # Eski ma'lumotlarni o'chirish
        CardTypeItem.objects.all().delete()
        CardTypeStatistics.objects.all().delete()

        factory = APIRequestFactory()

        request = factory.post(
            "/card-type-statistics/sync/"
        )

        response = SyncCardTypeStatisticsAPIView.as_view()(request)

        print("SUCCESS:", response.data)

    except Exception as e:

        print("ERROR:", str(e))