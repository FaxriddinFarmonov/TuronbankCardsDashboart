
from django.http import JsonResponse
from django.views import View

from django.db.models import Count, Q

from apps.cards.models import ActiveCard

# =========================================================
# CARD CATEGORY SERVICE
# =========================================================
class CardCategoryService:
    """
    Senior Level Card Category Analytics

    FEATURES:
    - Ultra Fast
    - Aggregation Optimized
    - Enterprise Architecture
    - Dashboard Ready
    - Frontend Ready
    - 600k+ rows optimized
    """

    # =====================================================
    # MAIN METHOD
    # =====================================================
    @classmethod
    def get_card_category_statistics(cls):

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

                "statistics": []
            }

        # =================================================
        # BASE QUERYSET
        # =================================================
        queryset = ActiveCard.objects.all()

        # =================================================
        # SALARY CARDS
        # =================================================
        salary_cards = (

            queryset

            .filter(

                Q(card_type__icontains="Зарплатная")

                |

                Q(card_type__icontains="Зарплатные")

            )

            .count()

        )

        # =================================================
        # VIRTUAL CARDS
        # =================================================
        virtual_cards = (

            queryset

            .filter(
                card_type__icontains="Виртуальная"
            )

            .count()

        )

        # =================================================
        # PENSION CARDS
        # =================================================
        pension_cards = (

            queryset

            .filter(
                card_type__icontains="пенсион"
            )

            .count()

        )

        # =================================================
        # PHYSICAL PERSON
        # =================================================
        physical_person_cards = (

            queryset

            .filter(
                client_type="Физ. лицо"
            )

            .count()

        )

        # =================================================
        # PHYSICAL CARDS
        # =================================================
        physical_cards = (

            physical_person_cards

            -

            (
                salary_cards
                +
                virtual_cards
                +
                pension_cards
            )
        )

        # =================================================
        # IP CARDS
        # =================================================
        ip_cards = (

            queryset

            .filter(
                client_type="ИП"
            )

            .count()

        )

        # =================================================
        # LEGAL ENTITY CARDS
        # =================================================
        legal_cards = (

            queryset

            .filter(
                client_type__icontains="Юр"
            )

            .count()

        )

        # =================================================
        # RESPONSE
        # =================================================
        response = [

            # =============================================
            # SALARY
            # =============================================
            {

                "category": "Зарплатная",

                "cards_count": salary_cards,

                "percentage": round(

                    (
                        salary_cards / total_cards
                    ) * 100,

                    2
                )
            },

            # =============================================
            # VIRTUAL
            # =============================================
            {

                "category": "Виртуальная",

                "cards_count": virtual_cards,

                "percentage": round(

                    (
                        virtual_cards / total_cards
                    ) * 100,

                    2
                )
            },

            # =============================================
            # PENSION
            # =============================================
            {

                "category": "Пенсионная",

                "cards_count": pension_cards,

                "percentage": round(

                    (
                        pension_cards / total_cards
                    ) * 100,

                    2
                )
            },

            # =============================================
            # PHYSICAL CARDS
            # =============================================
            {

                "category": "Физ-карта",

                "cards_count": physical_cards,

                "percentage": round(

                    (
                        physical_cards / total_cards
                    ) * 100,

                    2
                )
            },

            # =============================================
            # IP
            # =============================================
            {

                "category": "Юр. лицо",

                "cards_count": ip_cards,

                "percentage": round(

                    (
                        ip_cards / total_cards
                    ) * 100,

                    2
                )
            },

            # =============================================
            # LEGAL
            # =============================================
            {

                "category": "ИП",

                "cards_count": legal_cards,

                "percentage": round(

                    (
                        legal_cards / total_cards
                    ) * 100,

                    2
                )
            },
        ]

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

            "statistics": response,
        }

class CardCategoryView(View):

    def get(self, request):

        data = (

            CardCategoryService
            .get_card_category_statistics()

        )

        return JsonResponse(
            data,
            safe=False
        )