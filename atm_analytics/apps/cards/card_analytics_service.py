
from django.http import JsonResponse
from django.views import View

from django.db.models import Count

from apps.cards.models import ActiveCard


# =========================================================
# ANALYTICS SERVICE
# =========================================================
class AnalyticsService:
    """
    Senior Level Analytics Service

    FEATURES:
    - Ultra Fast
    - Minimal Queries
    - Aggregation Optimized
    - Frontend Ready
    - Dashboard Ready
    - Enterprise Architecture
    """

    # =====================================================
    # CARD STATUS
    # =====================================================
    @classmethod
    def get_card_status_statistics(cls, total_cards):

        queryset = (

            ActiveCard.objects

            .values("card_status")

            .annotate(
                cards_count=Count("id")
            )

            .order_by("-cards_count")

        )

        response = []

        for item in queryset:

            percentage = round(

                (
                    item["cards_count"]
                    / total_cards
                ) * 100,

                2
            )

            response.append({

                "card_status": (
                    item["card_status"]
                    or "UNKNOWN"
                ),

                "cards_count": item["cards_count"],

                "percentage": percentage,
            })

        return response

    # =====================================================
    # RESIDENT STATUS
    # =====================================================
    @classmethod
    def get_resident_statistics(cls, total_cards):

        queryset = (

            ActiveCard.objects

            .values("resident_status")

            .annotate(
                cards_count=Count("id")
            )

            .order_by("-cards_count")

        )

        response = []

        for item in queryset:

            status = item["resident_status"]

            # =============================================
            # TITLE
            # =============================================
            if status == "1":

                title = "Rezident"

            elif status == "0":

                title = "Nerezident"

            else:

                title = "Unknown"

            # =============================================
            # PERCENTAGE
            # =============================================
            percentage = round(

                (
                    item["cards_count"]
                    / total_cards
                ) * 100,

                2
            )

            response.append({

                "resident_status": status,

                "title": title,

                "cards_count": item["cards_count"],

                "percentage": percentage,
            })

        return response

    # =====================================================
    # CLIENT TYPE
    # =====================================================
    @classmethod
    def get_client_type_statistics(cls, total_cards):

        queryset = (

            ActiveCard.objects

            .values("client_type")

            .annotate(
                cards_count=Count("id")
            )

            .order_by("-cards_count")

        )

        response = []

        for item in queryset:

            percentage = round(

                (
                    item["cards_count"]
                    / total_cards
                ) * 100,

                2
            )

            response.append({

                "client_type": (
                    item["client_type"]
                    or "UNKNOWN"
                ),

                "cards_count": item["cards_count"],

                "percentage": percentage,
            })

        return response

    # =====================================================
    # MAIN ANALYTICS
    # =====================================================
    @classmethod
    def get_all_statistics(cls):

        # =================================================
        # TOTAL CARDS
        # =================================================
        total_cards = ActiveCard.objects.count()

        # =================================================
        # EMPTY PROTECTION
        # =================================================
        if total_cards == 0:

            return {

                "total_cards": 0,

                "card_status_statistics": [],

                "resident_statistics": [],

                "client_type_statistics": [],
            }

        # =================================================
        # RESPONSE
        # =================================================
        return {

            "total_cards": total_cards,

            # =============================================
            # CARD STATUS
            # =============================================
            "card_status_statistics":

                cls.get_card_status_statistics(
                    total_cards
                ),

            # =============================================
            # RESIDENT
            # =============================================
            "resident_statistics":

                cls.get_resident_statistics(
                    total_cards
                ),

            # =============================================
            # CLIENT TYPE
            # =============================================
            "client_type_statistics":

                cls.get_client_type_statistics(
                    total_cards
                ),
        }




class AnalyticsView(View):

    def get(self, request):

        data = (
            AnalyticsService
            .get_all_statistics()
        )

        return JsonResponse(
            data,
            safe=False
        )