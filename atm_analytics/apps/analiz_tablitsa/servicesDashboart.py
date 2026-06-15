from .models import DashboardStatistics, HeadOfficeItem
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIRequestFactory

import requests
from django.core.management.base import BaseCommand



def save_dashboard_data(data: dict):
    obj = DashboardStatistics.objects.create(
        total_cards=data["total_cards"],
        active_cards=data["active_cards"],
        active_percent=data["active_percent"],
        noactive_cards=data["noactive_cards"],
        noactive_percent=data["noactive_percent"],

        virtual_cards_count=data["virtual_cards"]["count"],
        virtual_cards_percent=data["virtual_cards"]["percent"],

        uzs_total_balance=data["uzs"]["total_balance"],
        uzs_average_balance=data["uzs"]["average_balance"],
        uzs_cards_count=data["uzs"]["cards_count"],

        usd_total_balance=data["usd"]["total_balance"],
        usd_average_balance=data["usd"]["average_balance"],
        usd_cards_count=data["usd"]["cards_count"],
    )

    return obj

from rest_framework.views import APIView
from rest_framework.response import Response
import requests



class SyncDashboardAPIView(APIView):

    def get(self, request):

        # 1. tashqi API dan olish
        response = requests.get("http://127.0.0.1:8000/dashboard/")
        data = response.json()

        # 2. DB ga saqlash
        obj = save_dashboard_data(data)

        return Response({
            "message": "saved successfully",
            "id": obj.id
        })



class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        data = requests.get(
            "http://127.0.0.1:8000/head-office-activity/"
        ).json()

        report = HeadOfficeActivity.objects.create(
            active_days=data["active_days"],
            total_active_cards=data["total_active_cards"]
        )

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

        self.stdout.write(self.style.SUCCESS("Synced successfully"))





def sync_dashboard_cron():

    try:
        factory = APIRequestFactory()

        request = factory.get("/dashboard/sync/")

        response = SyncDashboardAPIView.as_view()(request)

        print("SUCCESS:", response.data)

    except Exception as e:
        print("ERROR:", str(e))