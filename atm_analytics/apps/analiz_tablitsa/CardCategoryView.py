
import requests
from rest_framework.views import APIView
from rest_framework.test import APIRequestFactory





def save_card_category_statistics(data: dict):

    report = CardCategoryReport.objects.create(
        total_cards=data["total_cards"]
    )

    items = [
        CardCategoryItem(
            report=report,
            category=i["category"],
            cards_count=i["cards_count"],
            percentage=i["percentage"]
        )
        for i in data["statistics"]
    ]

    CardCategoryItem.objects.bulk_create(items)

    return report


class SyncCardCategoryAPIView(APIView):

    def post(self, request):

        data = requests.get(
            "http://127.0.0.1:8000/card-category-statistics/"
        ).json()

        report = save_card_category_statistics(data)

        return Response({
            "message": "synced successfully",
            "report_id": report.id
        })


from rest_framework.views import APIView
from rest_framework.response import Response

from .models import CardCategoryReport, CardCategoryItem


class CardCategoryAPIView(APIView):

    def get(self, request):

        report = CardCategoryReport.objects.prefetch_related(
            "statistics"
        ).first()

        if not report:
            return Response({"message": "no data"}, status=404)

        return Response({
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


def sync_card_category_cron():

    try:

        factory = APIRequestFactory()

        request = factory.post(
            "/card-category-statistics/sync/"
        )

        response = SyncCardCategoryAPIView.as_view()(request)

        print("SUCCESS:", response.data)

    except Exception as e:

        print("ERROR:", str(e))