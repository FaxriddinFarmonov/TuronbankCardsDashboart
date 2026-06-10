
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
# ACTIVITY PERIOD SERVICE
# =========================================================
class ActivityPeriodService:
    """
    Senior Level Activity Analytics

    FEATURES:
    - Ultra Fast
    - Optimized Queries
    - Aggregation Ready
    - Dashboard Ready
    - Enterprise Architecture
    - 600k+ rows optimized
    """

    # =====================================================
    # MAIN METHOD
    # =====================================================
    @classmethod
    def get_activity_statistics(cls):

        # =================================================
        # TODAY
        # =================================================
        today = timezone.now().date()

        # =================================================
        # DATE LIMITS
        # =================================================
        days_30 = today - timedelta(days=30)

        days_90 = today - timedelta(days=90)

        days_180 = today - timedelta(days=180)

        # =================================================
        # BASE QUERYSET
        # =================================================
        queryset = ActiveCard.objects.all()

        # =================================================
        # TOTAL CARDS
        # =================================================
        total_cards = queryset.count()

        # =================================================
        # EMPTY PROTECTION
        # =================================================
        if total_cards == 0:

            return {

                "today": str(today),

                "total_cards": 0,

                "statistics": []
            }

        # =================================================
        # ACTIVITY RANGES
        # =================================================
        activity_ranges = [

            # =============================================
            # 0 - 30 DAYS
            # =============================================
            {
                "title": "0 - 30 kun",

                "filter": (

                    Q(
                        dt_turnover__gte=days_30
                    )

                    |

                    Q(
                        ct_turnover__gte=days_30
                    )
                )
            },

            # =============================================
            # 30 - 90 DAYS
            # =============================================
            {
                "title": "30 - 90 kun",

                "filter": (

                    (

                        Q(
                            dt_turnover__lt=days_30
                        )

                        &

                        Q(
                            dt_turnover__gte=days_90
                        )

                    )

                    |

                    (

                        Q(
                            ct_turnover__lt=days_30
                        )

                        &

                        Q(
                            ct_turnover__gte=days_90
                        )

                    )
                )
            },

            # =============================================
            # 90 - 180 DAYS
            # =============================================
            {
                "title": "90 - 180 kun",

                "filter": (

                    (

                        Q(
                            dt_turnover__lt=days_90
                        )

                        &

                        Q(
                            dt_turnover__gte=days_180
                        )

                    )

                    |

                    (

                        Q(
                            ct_turnover__lt=days_90
                        )

                        &

                        Q(
                            ct_turnover__gte=days_180
                        )

                    )
                )
            },

            # =============================================
            # 180+ DAYS
            # =============================================
            {
                "title": "180+ kun",

                "filter": (

                    (

                        Q(
                            dt_turnover__lt=days_180
                        )

                    )

                    |

                    (

                        Q(
                            ct_turnover__lt=days_180
                        )

                    )
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
        for item in activity_ranges:

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
            # PUSH
            # =============================================
            response.append({

                "period": item["title"],

                "cards_count": cards_count,

                "percentage": percentage,
            })

        # =================================================
        # FINAL RESPONSE
        # =================================================
        return {

            "today": str(today),

            "total_cards": total_cards,

            "statistics": response,
        }



class ActivityPeriodView(View):

    def get(self, request):

        data = (

            ActivityPeriodService
            .get_activity_statistics()

        )

        return JsonResponse(
            data,
            safe=False
        )