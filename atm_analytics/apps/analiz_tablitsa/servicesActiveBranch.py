
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from .models import HeadOfficeActivity, HeadOfficeItem



def save_head_office_activity(data: dict):

    report = HeadOfficeActivity.objects.create(
        active_days=data["active_days"],
        total_active_cards=data["total_active_cards"]
    )

    offices = [
        HeadOfficeItem(
            report=report,
            head_office=item["head_office"],
            active_cards=item["active_cards"],
            percentage=item["percentage"]
        )
        for item in data["head_offices"]
    ]

    HeadOfficeItem.objects.bulk_create(offices)

    return report

class SyncHeadOfficeActivityAPIView(APIView):

    def post(self, request):

        # 1. external API dan olish
        data = requests.get(
            "http://127.0.0.1:8000/head-office-activity/"
        ).json()

        # 2. DB ga yozish (header)
        report = HeadOfficeActivity.objects.create(
            active_days=data["active_days"],
            total_active_cards=data["total_active_cards"]
        )

        # 3. list ni yozish
        items = [
            HeadOfficeItem(
                report=report,
                head_office=i["head_office"],
                active_cards=i["active_cards"],
                percentage=i["percentage"]
            )
            for i in data["head_offices"]
        ]

        HeadOfficeItem.objects.bulk_create(items)

        return Response({
            "message": "Synced successfully",
            "report_id": report.id,
            "count": len(items)
        })



def sync_head_office_activity_cron():

    try:

        # Eski ma'lumotlarni tozalash
        HeadOfficeItem.objects.all().delete()
        HeadOfficeActivity.objects.all().delete()

        factory = APIRequestFactory()

        request = factory.post(
            "/head-office-activity/sync/"
        )

        response = SyncHeadOfficeActivityAPIView.as_view()(request)

        print("SUCCESS:", response.data)

    except Exception as e:

        print("ERROR:", str(e))