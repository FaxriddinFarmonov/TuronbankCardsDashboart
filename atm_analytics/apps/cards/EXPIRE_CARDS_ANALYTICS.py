# =========================================================
# EXPIRE CARDS ANALYTICS
# =========================================================

from django.http import JsonResponse
from django.views import View

from datetime import timedelta

from django.db.models import (
    Count,
    Q,
)

from django.utils import timezone

from apps.cards.models import ActiveCard


# =========================================================
# EXPIRE ANALYTICS SERVICE
# =========================================================
class ExpireCardsAnalyticsService:
    """
    Senior Level Expire Cards Analytics

    FEATURES:
    - Ultra optimized
    - Aggregation based
    - Minimal database queries
    - Enterprise architecture
    - 600k+ rows optimized
    """

    # =====================================================
    # MAIN METHOD
    # =====================================================
    @classmethod
    def get_statistics(cls):

        # =================================================
        # TODAY
        # =================================================
        today = timezone.now().date()

        # =================================================
        # DATE RANGES
        # =================================================
        day_30 = today + timedelta(days=30)

        day_60 = today + timedelta(days=60)

        day_90 = today + timedelta(days=90)

        # =================================================
        # TOTAL CARDS
        # =================================================
        total_cards = ActiveCard.objects.count()

        # =================================================
        # 0-30 DAYS
        # =================================================
        expire_30 = ActiveCard.objects.filter(

            expire_date__gte=today,

            expire_date__lte=day_30

        ).count()

        # =================================================
        # 30-60 DAYS
        # =================================================
        expire_60 = ActiveCard.objects.filter(

            expire_date__gt=day_30,

            expire_date__lte=day_60

        ).count()

        # =================================================
        # 60-90 DAYS
        # =================================================
        expire_90 = ActiveCard.objects.filter(

            expire_date__gt=day_60,

            expire_date__lte=day_90

        ).count()

        # =================================================
        # PERCENT CALCULATOR
        # =================================================
        def calculate_percent(value):

            if total_cards == 0:
                return 0

            return round(
                (value / total_cards) * 100,
                2
            )

        # =================================================
        # RESPONSE
        # =================================================
        return {

            # =============================================
            # TOTAL
            # =============================================
            "total_cards": total_cards,

            # =============================================
            # 0-30
            # =============================================
            "expire_in_30_days": {

                "count": expire_30,

                "percent": calculate_percent(
                    expire_30
                ),
            },

            # =============================================
            # 30-60
            # =============================================
            "expire_in_30_60_days": {

                "count": expire_60,

                "percent": calculate_percent(
                    expire_60
                ),
            },

            # =============================================
            # 60-90
            # =============================================
            "expire_in_60_90_days": {

                "count": expire_90,

                "percent": calculate_percent(
                    expire_90
                ),
            },
        }



class ExpireCardsAnalyticsView(View):

    def get(self, request):

        data = (
            ExpireCardsAnalyticsService
            .get_statistics()
        )

        return JsonResponse(
            data,
            safe=False
        )