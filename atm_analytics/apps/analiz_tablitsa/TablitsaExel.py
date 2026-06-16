import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory




from .models import (
    BranchDashboardReport,
    BranchDashboardItem,
    BranchCardTypeStat,
    BranchBalance,
    BranchDormantStat
)


def save_branch_dashboard(data: dict):

    report = BranchDashboardReport.objects.create(
        total_cards=data["total_cards"]
    )

    for branch in data["branches"]:

        item = BranchDashboardItem.objects.create(
            report=report,
            head_office=branch["head_office"],
            total_cards=branch["total_cards"],
            active_cards=branch["active_cards"],
            active_percentage=branch["active_percentage"]
        )

        # CARD TYPES
        for ctype, value in branch["card_types"].items():
            BranchCardTypeStat.objects.create(
                branch=item,
                card_type=ctype,
                total=value["total"],
                active=value["active"]
            )

        # BALANCES
        BranchBalance.objects.create(
            branch=item,
            uzs=branch["balances"]["uzs"],
            usd=branch["balances"]["usd"]
        )

        # DORMANT
        BranchDormantStat.objects.create(
            branch=item,
            count=branch["dormant"]["count"],
            percentage=branch["dormant"]["percentage"],
            uzs_cards=branch["dormant"]["uzs_cards"],
            usd_cards=branch["dormant"]["usd_cards"]
        )

    return report



class SyncBranchDashboardAPIView(APIView):

    BranchDashboardReport.objects.all().delete()   # eski malumotlar ochirilib kn yangisi qoyiladi
    BranchDashboardItem.objects.all().delete()
    BranchCardTypeStat.objects.all().delete()
    BranchBalance.objects.all().delete()
    BranchDormantStat.objects.all().delete()

    def post(self, request):

        data = requests.get(
            "http://127.0.0.1:8000/branch-dashboard/"
        ).json()

        report = save_branch_dashboard(data)

        return Response({
            "message": "branch dashboard synced successfully",
            "report_id": report.id
        })

class BranchDashboardAPIView(APIView):

    def get(self, request):

        report = BranchDashboardReport.objects.prefetch_related(
            "branches__card_types",
            "branches__balances",
            "branches__dormant"
        ).first()

        if not report:
            return Response({"message": "no data"}, status=404)

        return Response({
            "total_cards": report.total_cards,

            "branches": [
                {
                    "head_office": b.head_office,
                    "total_cards": b.total_cards,
                    "active_cards": b.active_cards,
                    "active_percentage": float(b.active_percentage),

                    "card_types": {
                        c.card_type: {
                            "total": c.total,
                            "active": c.active
                        }
                        for c in b.card_types.all()
                    },

                    "balances": {
                        "uzs": str(b.balances.uzs),
                        "usd": str(b.balances.usd)
                    },

                    "dormant": {
                        "count": b.dormant.count,
                        "percentage": float(b.dormant.percentage),
                        "uzs_cards": b.dormant.uzs_cards,
                        "usd_cards": b.dormant.usd_cards
                    }
                }
                for b in report.branches.all()
            ]
        })


def sync_branch_dashboard_cron():

    try:

        # CHILD TABLELAR


        factory = APIRequestFactory()

        request = factory.post(
            "/branch-dashboard/sync/"
        )

        response = SyncBranchDashboardAPIView.as_view()(request)

        print("SUCCESS:", response.data)

    except Exception as e:
        print("ERROR:", str(e))

