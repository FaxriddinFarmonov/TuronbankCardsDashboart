from django.urls import path

from .BranchActive import HeadOfficeActivityView, HeadOfficeActivityService
from .EXPIRE_CARDS_ANALYTICS import ExpireCardsAnalyticsView
from .MONTHLY_CARD_ISSUED_ANALYTICS import MonthlyIssuedCardsAnalyticsView
from .activity_period_service import ActivityPeriodView
from .balance_statistics_service import BalanceStatisticsView
from .branch_tablitsa_service import BranchDashboardView
from .card_analytics_service import AnalyticsView
from .card_category_service import CardCategoryView
from .card_type_statistics_service import CardTypeStatisticsView
from .views import DashboardStatisticsView
from django.contrib import admin

admin.site.site_header = "Turonbank boshqaruv paneli"
admin.site.site_title = "Boshqaruv Paneli"
admin.site.index_title = "Xush kelibsiz!"

urlpatterns = [

    path(
        "dashboard/",
        DashboardStatisticsView.as_view(),
        name="dashboard"
    ),
    path(
        "head-office-activity/",
        HeadOfficeActivityView.as_view(),
        name="head_office_activity"
    ),

    path(
        "card-type-statistics/",
        CardTypeStatisticsView.as_view(),
        name="card_type_statistics"
    ),
    path(
            "analytics/",
            AnalyticsView.as_view(),
            name="analytics"
        ),
    path(
        "balance-statistics/",
        BalanceStatisticsView.as_view(),
        name="balance_statistics"
    ),
    path(
        "activity-period-statistics/",
        ActivityPeriodView.as_view(),
        name="activity_period_statistics"
    ),
    path(
        "card-category-statistics/",
        CardCategoryView.as_view(),
        name="card_category_statistics"
    ),
    path(
        "expire-cards/",
        ExpireCardsAnalyticsView.as_view(),
        name="expire_cards"
    ),
    path(
            "monthly-issued-cards/",
            MonthlyIssuedCardsAnalyticsView.as_view(),
            name="monthly_issued_cards"
        ),
    path(
        "branch-dashboard/",
        BranchDashboardView.as_view(),
        name="branch-dashboard"
    ),


]