from django.urls import path

from .ActivityPeriodCardView import ActivityPeriodAPIView, SyncActivityPeriodAPIView
from .AnaliticView import AnalyticsAPIView, SyncAnalyticsAPIView
from .BalanceStaticView import BalanceStatisticsAPIView, SyncBalanceStatisticsAPIView
from .CardCategoryView import CardCategoryAPIView, SyncCardCategoryAPIView
from .CardTypeView import CardTypeStatisticsAPIView, SyncCardTypeStatisticsAPIView
from .ExpireCardsView import ExpireCardsAPIView, SyncExpireCardsAPIView
from .MonthlyView import MonthlyIssuedCardsAPIView, SyncMonthlyIssuedCardsAPIView
from .TablitsaExel import BranchDashboardAPIView, SyncBranchDashboardAPIView
from .apiFrontActiveBranch import HeadOfficeActivityAPIView
from  .dashboart_view import DashboardStatisticsAPIView
from .funk_cron import SyncAllDashboardsAPIView
from .servicesActiveBranch import SyncHeadOfficeActivityAPIView
from .servicesDashboart import SyncDashboardAPIView

urlpatterns = [
    path("dashboard/", DashboardStatisticsAPIView.as_view(), name="dashboard"),
    path("dashboard/sync/", SyncDashboardAPIView.as_view(), name="sync"),

    path("head-office-activity/",HeadOfficeActivityAPIView.as_view(),name="head-office-activity" ),
    path("head-office-activity/sync/",SyncHeadOfficeActivityAPIView.as_view(),name="sync-head-office-activity" ),

    path(
        "card-type-statistics/",
        CardTypeStatisticsAPIView.as_view(),
        name="card-type-statistics",
    ),
    path(
        "card-type-statistics/sync/",
        SyncCardTypeStatisticsAPIView.as_view(),
        name="sync-card-type-statistics",
    ),
    path(
        "sync-all-dashboards/",
        SyncAllDashboardsAPIView.as_view(),
        name="sync-all-dashboards"
    ),

    path("analytics/", AnalyticsAPIView.as_view()),
    path("analytics/sync/", SyncAnalyticsAPIView.as_view()),

    path("balance-statistics/", BalanceStatisticsAPIView.as_view()),
    path("balance-statistics/sync/", SyncBalanceStatisticsAPIView.as_view()),

    path("activity-period-statistics/", ActivityPeriodAPIView.as_view()),
    path("activity-period-statistics/sync/", SyncActivityPeriodAPIView.as_view()),

    path("card-category-statistics/", CardCategoryAPIView.as_view()),
    path("card-category-statistics/sync/", SyncCardCategoryAPIView.as_view()),

    path("expire-cards/", ExpireCardsAPIView.as_view()),
    path("expire-cards/sync/", SyncExpireCardsAPIView.as_view()),

    path("monthly-issued-cards/", MonthlyIssuedCardsAPIView.as_view()),
    path("monthly-issued-cards/sync/", SyncMonthlyIssuedCardsAPIView.as_view()),

    path("branch-dashboard/", BranchDashboardAPIView.as_view()),
    path("branch-dashboard/sync/", SyncBranchDashboardAPIView.as_view()),
]