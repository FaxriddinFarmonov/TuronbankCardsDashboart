
from django.http import JsonResponse
from django.views import View

from django.db.models import (
    Count,
    Q,
)

from apps.cards.models import ActiveCard


# =========================================================
# CARD TYPE STATISTICS SERVICE
# =========================================================
class CardTypeStatisticsService:
    """
    Senior Level Card Type Analytics

    FEATURES:
    - Ultra Fast
    - Aggregation Optimized
    - Frontend Ready
    - Pie Chart Ready
    - Enterprise Architecture
    """

    # =====================================================
    # CARD SYSTEM GROUPS
    # =====================================================
    CARD_GROUPS = {

        # ================================================
        # HUMO
        # ================================================
        "HUMO": [
            "HUMO1",
        ],

        # ================================================
        # UZCARD
        # ================================================
        "UZCARD": [

            "UZBCBJDUO",

            "UZCARD",

            "MIR",
        ],

        # ================================================
        # VISA
        # ================================================
        "VISA": [

            "VISA BSN",

            "VISA CL DT",

            "VISA CL EX",

            "VISA CL VI",

            "VISA GDE",

            "VISA GOLD",
        ],

        # ================================================
        # MASTER CARD
        # ================================================
        "MASTER CARD": [

            "MC GL TURN",

            "MC GLD TUR",

            "MC GOLD",

            "MC ST VI",

            "MC Standar",
        ],
    }

    # =====================================================
    # MAIN METHOD
    # =====================================================
    @classmethod
    def get_card_type_statistics(cls):

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

                "card_types": []
            }

        # =================================================
        # RESPONSE
        # =================================================
        response = []

        # =================================================
        # LOOP CARD GROUPS
        # =================================================
        for card_type, systems in cls.CARD_GROUPS.items():

            # =============================================
            # COUNT
            # =============================================
            cards_count = (

                ActiveCard.objects

                .filter(
                    card_system__in=systems
                )

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

                "card_type": card_type,

                "cards_count": cards_count,

                "percentage": percentage,

                "systems": systems,
            })

        # =================================================
        # SORT
        # =================================================
        response.sort(
            key=lambda x: x["cards_count"],
            reverse=True
        )

        # =================================================
        # FINAL RESPONSE
        # =================================================
        return {

            "total_cards": total_cards,

            "card_types": response,
        }




class CardTypeStatisticsView(View):

    def get(self, request):

        data = (

            CardTypeStatisticsService
            .get_card_type_statistics()

        )

        return JsonResponse(
            data,
            safe=False
        )