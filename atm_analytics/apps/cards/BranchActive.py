
from django.utils import timezone

from apps.cards.models import ActiveCard

from django.http import JsonResponse
from django.views import View

from datetime import timedelta

from django.db.models import (
    Count,
    Q,
)

from apps.cards.branch_tablitsa_service import MAIN_HEAD_OFFICES


# =========================================================
# HEAD OFFICES
# =========================================================



# =========================================================
# HEAD OFFICE ACTIVITY SERVICE
# =========================================================
class HeadOfficeActivityService:
    """
    Senior Level Head Office Analytics

    FEATURES:
    - Ultra Fast

    - Aggregation Optimized
    - 600k+ rows optimized
    - Enterprise Architecture
    - Dashboard Ready
    - Pie Chart Ready
    """

    # =====================================================
    # ACTIVE DAYS
    # =====================================================
    ACTIVE_DAYS = 90

    # =====================================================
    # MAIN METHOD
    # =====================================================
    @classmethod
    def get_head_office_activity(cls):

        # =================================================
        # TODAY
        # =================================================
        today = timezone.now().date()

        # =================================================
        # ACTIVE LIMIT DATE
        # =================================================
        active_limit_date = today - timedelta(
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
        # TOTAL ACTIVE CARDS
        # =================================================
        total_active_cards = (

            ActiveCard.objects

            .filter(
                active_filter
            )

            .count()
        )

        # =================================================
        # EMPTY PROTECTION
        # =================================================
        if total_active_cards == 0:

            return {

                "total_active_cards": 0,

                "head_offices": []
            }

        # =================================================
        # GROUP BY HEAD OFFICE
        # =================================================
        queryset = (

            ActiveCard.objects

            .filter(

                active_filter,

                head_office__in=MAIN_HEAD_OFFICES
            )

            .values(
                "head_office"
            )

            .annotate(

                active_cards=Count("id")

            )

            .order_by("-active_cards")
        )

        # =================================================
        # RESPONSE
        # =================================================
        response = []

        for item in queryset:

            percentage = round(

                (
                    item["active_cards"]
                    / total_active_cards
                ) * 100,

                2
            )

            response.append({

                "head_office": item["head_office"],

                "active_cards": item["active_cards"],

                "percentage": percentage,
            })

        # =================================================
        # FINAL RESPONSE
        # =================================================
        return {

            "active_days": cls.ACTIVE_DAYS,

            "total_active_cards": total_active_cards,

            "head_offices": response,
        }


class HeadOfficeActivityView(View):

    def get(self, request):

        data = (
            HeadOfficeActivityService
            .get_head_office_activity()
        )

        return JsonResponse(
            data,
            safe=False
        )
