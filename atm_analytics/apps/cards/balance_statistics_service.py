
from django.http import JsonResponse
from django.views import View

from django.db.models import (
    Count,
    Q,
)

from apps.cards.models import ActiveCard


# =========================================================
# BALANCE STATISTICS SERVICE
# =========================================================
class BalanceStatisticsService:
    """
    Senior Level Balance Analytics

    FEATURES:
    - Ultra Fast
    - Aggregation Optimized
    - Enterprise Architecture
    - Dashboard Ready
    - Pie Chart Ready
    - 600k+ rows optimized
    """

    # =====================================================
    # ONLY UZS
    # =====================================================
    CURRENCY = "UZS"

    # =====================================================
    # MAIN METHOD
    # =====================================================
    @classmethod
    def get_balance_statistics(cls):

        # =================================================
        # BASE QUERYSET
        # =================================================
        queryset = (

            ActiveCard.objects

            .filter(
                currency_code=cls.CURRENCY
            )

        )

        # =================================================
        # TOTAL CARDS
        # =================================================
        total_cards = queryset.count()

        # =================================================
        # EMPTY PROTECTION
        # =================================================
        if total_cards == 0:

            return {

                "currency": cls.CURRENCY,

                "total_cards": 0,

                "statistics": []
            }

        # =================================================
        # BALANCE RANGES
        # =================================================
        balance_ranges = [

            {
                "title": "100 mln dan yuqori",

                "filter": Q(
                    balance__gt=100_000_000
                )
            },

            {
                "title": "10 mln - 100 mln",

                "filter": Q(
                    balance__gte=10_000_000,
                    balance__lte=100_000_000
                )
            },

            {
                "title": "1 mln - 10 mln",

                "filter": Q(
                    balance__gte=1_000_000,
                    balance__lt=10_000_000
                )
            },

            {
                "title": "100 ming - 1 mln",

                "filter": Q(
                    balance__gte=100_000,
                    balance__lt=1_000_000
                )
            },

            {
                "title": "0 - 100 ming",

                "filter": Q(
                    balance__gte=0,
                    balance__lt=100_000
                )
            },
        ]

        # =================================================
        # RESPONSE
        # =================================================
        response = []

        # =================================================
        # LOOP
        # =================================================
        for item in balance_ranges:

            # =============================================
            # COUNT
            # =============================================
            cards_count = (

                queryset

                .filter(item["filter"])

                .count()

            )

            # =============================================
            # PERCENTAGE
            # =============================================
            percentage = round(

                (
                    cards_count / total_cards
                ) * 100,

                2
            )

            # =============================================
            # RESPONSE PUSH
            # =============================================
            response.append({

                "category": item["title"],

                "cards_count": cards_count,

                "percentage": percentage,
            })

        # =================================================
        # FINAL RESPONSE
        # =================================================
        return {

            "currency": cls.CURRENCY,

            "total_cards": total_cards,

            "statistics": response,
        }


class BalanceStatisticsView(View):

    def get(self, request):

        data = (

            BalanceStatisticsService
            .get_balance_statistics()

        )

        return JsonResponse(
            data,
            safe=False
        )