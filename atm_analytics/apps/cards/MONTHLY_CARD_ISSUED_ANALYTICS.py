# =========================================================
# MONTHLY CARD ISSUED ANALYTICS
# =========================================================

from django.http import JsonResponse
from django.views import View

from django.db.models import Count
from django.db.models.functions import ExtractMonth

from django.utils import timezone

from apps.cards.models import ActiveCard


# =========================================================
# MONTH NAMES
# =========================================================
MONTHS = {

    1: "Yanvar",
    2: "Fevral",
    3: "Mart",
    4: "Aprel",
    5: "May",
    6: "Iyun",
    7: "Iyul",
    8: "Avgust",
    9: "Sentabr",
    10: "Oktabr",
    11: "Noyabr",
    12: "Dekabr",
}


# =========================================================
# SERVICE
# =========================================================
class MonthlyIssuedCardsAnalyticsService:
    """
    Senior Level Monthly Analytics

    FEATURES:
    - Ultra optimized
    - Aggregation based
    - Minimal queries
    - Enterprise architecture
    - 600k+ rows optimized
    """

    # =====================================================
    # MAIN METHOD
    # =====================================================
    @classmethod
    def get_statistics(cls):

        # =================================================
        # CURRENT YEAR
        # =================================================
        current_year = timezone.now().year

        # =================================================
        # QUERY
        # =================================================
        queryset = (

            ActiveCard.objects

            .filter(
                doc_date__year=current_year
            )

            .annotate(
                month=ExtractMonth("doc_date")
            )

            .values("month")

            .annotate(
                total=Count("id")
            )

            .order_by("month")
        )

        # =================================================
        # DEFAULT DATA
        # =================================================
        monthly_data = {

            MONTHS[i]: 0
            for i in range(1, 13)
        }

        # =================================================
        # FILL DATA
        # =================================================
        for item in queryset:

            month_number = item["month"]

            total = item["total"]

            month_name = MONTHS.get(
                month_number
            )

            monthly_data[month_name] = total

        # =================================================
        # RESPONSE
        # =================================================
        return {

            "year": current_year,

            "monthly_cards": monthly_data,
        }


# =========================================================
# API VIEW
# =========================================================
class MonthlyIssuedCardsAnalyticsView(View):

    def get(self, request):

        data = (

            MonthlyIssuedCardsAnalyticsService
            .get_statistics()

        )

        return JsonResponse(
            data,
            safe=False
        )