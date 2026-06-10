from django.core.management.base import BaseCommand

from ..analytics.models import DashboardStatistics


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        data = {
            "total_cards": 576006,
            "active_cards": 188867,
            "active_percent": 32.79,
            "noactive_cards": 387139,
            "noactive_percent": 67.21,
            "virtual_cards": {
                "count": 114203,
                "percent": 19.83
            },
            "uzs": {
                "total_balance": "232117037835.090",
                "average_balance": "412832.32",
                "cards_count": 562255
            },
            "usd": {
                "total_balance": "1425979.40000000",
                "average_balance": "103.70",
                "cards_count": 13751
            }
        }

        DashboardStatistics.objects.create(
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

        self.stdout.write(
            self.style.SUCCESS(
                "Dashboard updated"
            )
        )