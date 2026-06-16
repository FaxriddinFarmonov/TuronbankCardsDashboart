from .ActivityPeriodCardView import sync_activity_period_cron
from .AnaliticView import sync_analytics_cron
from .BalanceStaticView import sync_balance_statistics_cron
from .CardCategoryView import sync_card_category_cron
from .CardTypeView import sync_card_type_statistics_cron
from .ExpireCardsView import sync_expire_cards_cron
from .MonthlyView import sync_monthly_issued_cards_cron
from .TablitsaExel import sync_branch_dashboard_cron
from .servicesActiveBranch import sync_head_office_activity_cron
from .servicesDashboart import sync_dashboard_cron






from rest_framework.views import APIView
from rest_framework.response import Response



class SyncAllDashboardsAPIView(APIView):

    def post(self, request):

        result = sync_all_crons()

        return Response(result)



def sync_all_crons():

    results = {}

    try:
        results["dashboard"] = sync_dashboard_cron()
        results["head_office"] = sync_head_office_activity_cron()
        results["card_type"] = sync_card_type_statistics_cron()
        results["analytics"] = sync_analytics_cron()
        results["balance"] = sync_balance_statistics_cron()
        results["activity_period"] = sync_activity_period_cron()
        results["card_category"] = sync_card_category_cron()
        results["expire_cards"] = sync_expire_cards_cron()
        results["monthly_cards"] = sync_monthly_issued_cards_cron()
        results["branch_dashboard"] = sync_branch_dashboard_cron()

        return {
            "status": "success",
            "message": "All cron jobs executed successfully",
            "results": results
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
            "results": results
        }