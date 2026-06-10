
from django.http import JsonResponse
from django.views import View


from datetime import timedelta

from django.db.models import (
    Count,
    Sum,
    Q,
)

from django.utils import timezone

from apps.cards.models import ActiveCard


# =========================================================
# MAIN HEAD OFFICES
# =========================================================
MAIN_HEAD_OFFICES = [

    "Андижон",
    "Бухоро",
    "Жиззах",
    "Зангиота",
    "Мирзо Улугбек",
    "Миробод",
    "Навоий",
    "Наманган",
    "Нукус",
    "Самарканд",
    "Сирдарё",
    "Сурхандарё",
    "Тошкент шахар",
    "Фаргона",
    "Хоразм",
    "Чилонзор",
    "Шахрисабз",
    "Юнусобод",
    "Қарши",
    "Булунгур",
]


# =========================================================
# CARD GROUPS
# =========================================================
CARD_GROUPS = {

    # =====================================================
    # HUMO
    # =====================================================
    "HUMO": [
        "HUMO1",
    ],

    # =====================================================
    # UZCARD
    # =====================================================
    "UZCARD": [

        "UZBCBJDUO",

        "UZCARD",

        "MIR",
    ],

    # =====================================================
    # VISA
    # =====================================================
    "VISA": [

        "VISA BSN",

        "VISA CL DT",

        "VISA CL EX",

        "VISA CL VI",

        "VISA GDE",

        "VISA GOLD",
    ],

    # =====================================================
    # MASTER CARD
    # =====================================================
    "MASTER CARD": [

        "MC GL TURN",

        "MC GLD TUR",

        "MC GOLD",

        "MC ST VI",

        "MC Standar",
    ],
}


# =========================================================
# BRANCH DASHBOARD SERVICE
# =========================================================
class BranchDashboardService:
    """
    ENTERPRISE LEVEL BRANCH DASHBOARD

    FEATURES:
    - Ultra Fast
    - Aggregation Based
    - Minimal Queries
    - Dashboard Ready
    - Frontend Ready
    - PieChart Ready
    - BarChart Ready
    - Enterprise Architecture
    """

    # =====================================================
    # ACTIVE DAYS
    # =====================================================
    ACTIVE_DAYS = 90

    # =====================================================
    # MAIN METHOD
    # =====================================================
    @classmethod
    def get_branch_dashboard(cls):

        # =================================================
        # TODAY
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
        # BASE QUERYSET
        # =================================================
        queryset = (

            ActiveCard.objects

            .filter(
                head_office__in=MAIN_HEAD_OFFICES
            )
        )

        # =================================================
        # TOTAL CARDS
        # =================================================
        total_cards_all = queryset.count()

        # =================================================
        # EMPTY PROTECTION
        # =================================================
        if total_cards_all == 0:

            return {
                "total_cards": 0,
                "branches": []
            }

        # =================================================
        # RESPONSE
        # =================================================
        response = []

        # =================================================
        # LOOP HEAD OFFICES
        # =================================================
        for head_office in MAIN_HEAD_OFFICES:

            # =============================================
            # BRANCH QUERYSET
            # =============================================
            branch_queryset = queryset.filter(
                head_office=head_office
            )

            # =============================================
            # TOTAL
            # =============================================
            total_cards = branch_queryset.count()

            # =============================================
            # ACTIVE
            # =============================================
            active_cards = branch_queryset.filter(
                active_filter
            ).count()

            # =============================================
            # ACTIVE %
            # =============================================
            active_percentage = 0

            if total_cards > 0:

                active_percentage = round(

                    (
                        active_cards
                        / total_cards
                    ) * 100,

                    2
                )

            # =============================================
            # DORMANT
            # =============================================
            dormant_cards = total_cards - active_cards

            # =============================================
            # DORMANT %
            # =============================================
            dormant_percentage = 0

            if total_cards > 0:

                dormant_percentage = round(

                    (
                        dormant_cards
                        / total_cards
                    ) * 100,

                    2
                )

            # =============================================
            # CARD TYPES
            # =============================================
            card_groups_data = {}

            for group_name, systems in CARD_GROUPS.items():

                # =========================================
                # TOTAL GROUP
                # =========================================
                group_total = (

                    branch_queryset

                    .filter(
                        card_system__in=systems
                    )

                    .count()
                )

                # =========================================
                # ACTIVE GROUP
                # =========================================
                group_active = (

                    branch_queryset

                    .filter(
                        card_system__in=systems
                    )

                    .filter(
                        active_filter
                    )

                    .count()
                )

                card_groups_data[group_name] = {

                    "total": group_total,

                    "active": group_active,
                }

            # =============================================
            # UZS BALANCE
            # =============================================
            uzs_balance = (

                branch_queryset

                .filter(
                    currency_code="UZS"
                )

                .aggregate(
                    total=Sum("balance")
                )
            )

            # =============================================
            # USD BALANCE
            # =============================================
            usd_balance = (

                branch_queryset

                .filter(
                    currency_code="USD"
                )

                .aggregate(
                    total=Sum("balance")
                )
            )

            # =============================================
            # DORMANT UZS
            # =============================================
            dormant_uzs = (

                branch_queryset

                .exclude(
                    active_filter
                )

                .filter(
                    currency_code="UZS"
                )

                .count()
            )

            # =============================================
            # DORMANT USD
            # =============================================
            dormant_usd = (

                branch_queryset

                .exclude(
                    active_filter
                )

                .filter(
                    currency_code="USD"
                )

                .count()
            )

            # =============================================
            # FINAL OBJECT
            # =============================================
            response.append({

                # =========================================
                # FILIAL
                # =========================================
                "head_office": head_office,

                # =========================================
                # TOTAL
                # =========================================
                "total_cards": total_cards,

                # =========================================
                # ACTIVE
                # =========================================
                "active_cards": active_cards,

                # =========================================
                # ACTIVE %
                # =========================================
                "active_percentage": active_percentage,

                # =========================================
                # CARD TYPES
                # =========================================
                "card_types": {

                    "HUMO": {
                        "total": (
                            card_groups_data["HUMO"]["total"]
                        ),
                        "active": (
                            card_groups_data["HUMO"]["active"]
                        ),
                    },

                    "UZCARD": {
                        "total": (
                            card_groups_data["UZCARD"]["total"]
                        ),
                        "active": (
                            card_groups_data["UZCARD"]["active"]
                        ),
                    },

                    "VISA": {
                        "total": (
                            card_groups_data["VISA"]["total"]
                        ),
                        "active": (
                            card_groups_data["VISA"]["active"]
                        ),
                    },

                    "MASTER_CARD": {
                        "total": (
                            card_groups_data["MASTER CARD"]["total"]
                        ),
                        "active": (
                            card_groups_data["MASTER CARD"]["active"]
                        ),
                    },
                },

                # =========================================
                # BALANCES
                # =========================================
                "balances": {

                    "uzs": (
                        uzs_balance["total"]
                        or 0
                    ),

                    "usd": (
                        usd_balance["total"]
                        or 0
                    ),
                },

                # =========================================
                # DORMANT
                # =========================================
                "dormant": {

                    "count": dormant_cards,

                    "percentage": dormant_percentage,

                    "uzs_cards": dormant_uzs,

                    "usd_cards": dormant_usd,
                },
            })

        # =================================================
        # SORT
        # =================================================
        response = sorted(

            response,

            key=lambda x: x["total_cards"],

            reverse=True
        )

        # =================================================
        # FINAL RESPONSE
        # =================================================
        return {

            "total_cards": total_cards_all,

            "branches": response
        }



# =========================================================
# BRANCH DASHBOARD VIEW
# =========================================================
class BranchDashboardView(View):

    def get(self, request):

        data = (
            BranchDashboardService
            .get_branch_dashboard()
        )

        return JsonResponse(
            data,
            safe=False
        )