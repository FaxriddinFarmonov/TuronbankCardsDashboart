# =========================================================
# DASHBOARD STATISTICS
# =========================================================

from django.http import JsonResponse
from django.views import View

from datetime import timedelta
from decimal import Decimal

from django.db.models import (
    Count,
    Sum,
    Avg,
    Q,
)

from django.utils import timezone

from apps.cards.models import ActiveCard


# =========================================================
# DASHBOARD STATISTICS SERVICE
# =========================================================
class DashboardStatisticsService:
    """
    Senior Level Dashboard Statistics Service

    - Ultra optimized
    - Aggregation based
    - Minimal queries
    - Enterprise architecture
    """

    ACTIVE_DAYS = 90

    # =====================================================
    # MAIN METHOD
    # =====================================================
    @classmethod
    def get_dashboard_statistics(cls):

        # =================================================
        # NOW DATE
        # =================================================
        now = timezone.now().date()

        active_limit_date = now - timedelta(
            days=cls.ACTIVE_DAYS
        )

        # =================================================
        # ACTIVE FILTER
        # =================================================
        active_filter = (

            Q(
                dt_turnover__gte=active_limit_date
            )

            |

            Q(
                ct_turnover__gte=active_limit_date
            )
        )

        # =================================================
        # TOTAL CARDS
        # =================================================
        total_cards = ActiveCard.objects.count()

        # =================================================
        # ACTIVE CARDS
        # =================================================
        active_cards = ActiveCard.objects.filter(
            active_filter
        ).count()

        # =================================================
        # NOACTIVE CARDS
        # =================================================
        noactive_cards = total_cards - active_cards

        # =================================================
        # ACTIVE %
        # =================================================
        active_percent = 0

        if total_cards > 0:

            active_percent = round(
                (active_cards / total_cards) * 100,
                2
            )

        # =================================================
        # NOACTIVE %
        # =================================================
        noactive_percent = 0

        if total_cards > 0:

            noactive_percent = round(
                (noactive_cards / total_cards) * 100,
                2
            )

        # =================================================
        # UZS STATISTICS
        # =================================================
        uzs_stats = ActiveCard.objects.filter(
            currency_code="UZS"
        ).aggregate(

            total_balance=Sum("balance"),

            avg_balance=Avg("balance"),

            cards_count=Count("id"),
        )

        # =================================================
        # USD STATISTICS
        # =================================================
        usd_stats = ActiveCard.objects.filter(
            currency_code="USD"
        ).aggregate(

            total_balance=Sum("balance"),

            avg_balance=Avg("balance"),

            cards_count=Count("id"),
        )

        # =================================================
        # VIRTUAL CARDS
        # =================================================
        virtual_cards = ActiveCard.objects.filter(
            card_type__icontains="Виртуальная"
        ).count()

        # =================================================
        # VIRTUAL %
        # =================================================
        virtual_percent = 0

        if total_cards > 0:

            virtual_percent = round(
                (virtual_cards / total_cards) * 100,
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
            # ACTIVE
            # =============================================
            "active_cards": active_cards,

            "active_percent": active_percent,

            # =============================================
            # NOACTIVE
            # =============================================
            "noactive_cards": noactive_cards,

            "noactive_percent": noactive_percent,

            # =============================================
            # VIRTUAL CARDS
            # =============================================
            "virtual_cards": {

                "count": virtual_cards,

                "percent": virtual_percent,
            },

            # =============================================
            # UZS
            # =============================================
            "uzs": {

                "total_balance": (
                    uzs_stats["total_balance"]
                    or Decimal("0")
                ),

                "average_balance": round(

                    uzs_stats["avg_balance"]
                    or Decimal("0"),

                    2
                ),

                "cards_count": (
                    uzs_stats["cards_count"]
                    or 0
                ),
            },

            # =============================================
            # USD
            # =============================================
            "usd": {

                "total_balance": (
                    usd_stats["total_balance"]
                    or Decimal("0")
                ),

                "average_balance": round(

                    usd_stats["avg_balance"]
                    or Decimal("0"),

                    2
                ),

                "cards_count": (
                    usd_stats["cards_count"]
                    or 0
                ),
            },
        }


# =========================================================
# API VIEW
# =========================================================
class DashboardStatisticsView(View):

    def get(self, request):

        data = DashboardStatisticsService.get_dashboard_statistics()

        return JsonResponse(
            data,
            safe=False
        )

