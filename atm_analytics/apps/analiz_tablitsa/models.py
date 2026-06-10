from django.db import models

# Create your models here.
from django.db import models


class DashboardStatistics(models.Model):
    total_cards = models.BigIntegerField()

    active_cards = models.BigIntegerField()
    active_percent = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    noactive_cards = models.BigIntegerField()
    noactive_percent = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    virtual_cards_count = models.BigIntegerField()
    virtual_cards_percent = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    uzs_total_balance = models.DecimalField(
        max_digits=30,
        decimal_places=3
    )

    uzs_average_balance = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    uzs_cards_count = models.BigIntegerField()

    usd_total_balance = models.DecimalField(
        max_digits=30,
        decimal_places=8
    )

    usd_average_balance = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    usd_cards_count = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']



class HeadOfficeActivity(models.Model):
    active_days = models.IntegerField()
    total_active_cards = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class HeadOfficeItem(models.Model):
    report = models.ForeignKey(
        HeadOfficeActivity,
        on_delete=models.CASCADE,
        related_name="head_offices"
    )

    head_office = models.CharField(max_length=255)
    active_cards = models.BigIntegerField()
    percentage = models.DecimalField(max_digits=10, decimal_places=2)

from django.db import models


class CardTypeStatistics(models.Model):
    total_cards = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class CardTypeItem(models.Model):
    report = models.ForeignKey(
        CardTypeStatistics,
        on_delete=models.CASCADE,
        related_name="card_types"
    )

    card_type = models.CharField(max_length=50)
    cards_count = models.BigIntegerField()
    percentage = models.DecimalField(max_digits=10, decimal_places=2)

    # list ichidagi systems
    systems = models.JSONField(default=list)



from django.db import models


class AnalyticsReport(models.Model):
    total_cards = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


# -------------------------
# CARD STATUS
# -------------------------
class CardStatusItem(models.Model):
    report = models.ForeignKey(
        AnalyticsReport,
        on_delete=models.CASCADE,
        related_name="card_status_statistics"
    )

    card_status = models.CharField(max_length=100)
    cards_count = models.BigIntegerField()
    percentage = models.DecimalField(max_digits=10, decimal_places=2)


# -------------------------
# RESIDENT
# -------------------------
class ResidentItem(models.Model):
    report = models.ForeignKey(
        AnalyticsReport,
        on_delete=models.CASCADE,
        related_name="resident_statistics"
    )

    resident_status = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    cards_count = models.BigIntegerField()
    percentage = models.DecimalField(max_digits=10, decimal_places=2)


# -------------------------
# CLIENT TYPE
# -------------------------
class ClientTypeItem(models.Model):
    report = models.ForeignKey(
        AnalyticsReport,
        on_delete=models.CASCADE,
        related_name="client_type_statistics"
    )

    client_type = models.CharField(max_length=100)
    cards_count = models.BigIntegerField()
    percentage = models.DecimalField(max_digits=10, decimal_places=2)


from django.db import models


class BalanceStatisticsReport(models.Model):
    currency = models.CharField(max_length=10)
    total_cards = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class BalanceStatisticsItem(models.Model):
    report = models.ForeignKey(
        BalanceStatisticsReport,
        on_delete=models.CASCADE,
        related_name="statistics"
    )

    category = models.CharField(max_length=100)
    cards_count = models.BigIntegerField()
    percentage = models.DecimalField(max_digits=10, decimal_places=2)




from django.db import models


class ActivityPeriodReport(models.Model):
    today = models.DateField()
    total_cards = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class ActivityPeriodItem(models.Model):
    report = models.ForeignKey(
        ActivityPeriodReport,
        on_delete=models.CASCADE,
        related_name="statistics"
    )

    period = models.CharField(max_length=50)
    cards_count = models.BigIntegerField()
    percentage = models.DecimalField(max_digits=10, decimal_places=2)




from django.db import models


class CardCategoryReport(models.Model):
    total_cards = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class CardCategoryItem(models.Model):
    report = models.ForeignKey(
        CardCategoryReport,
        on_delete=models.CASCADE,
        related_name="statistics"
    )

    category = models.CharField(max_length=100)
    cards_count = models.BigIntegerField()
    percentage = models.DecimalField(max_digits=10, decimal_places=2)


from django.db import models


class ExpireCardsReport(models.Model):
    total_cards = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class ExpireCardsItem(models.Model):
    report = models.ForeignKey(
        ExpireCardsReport,
        on_delete=models.CASCADE,
        related_name="expire_statistics"
    )

    period = models.CharField(max_length=50)
    count = models.BigIntegerField()
    percent = models.DecimalField(max_digits=10, decimal_places=2)



from django.db import models


class MonthlyIssuedCardsReport(models.Model):
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class MonthlyIssuedCardsItem(models.Model):
    report = models.ForeignKey(
        MonthlyIssuedCardsReport,
        on_delete=models.CASCADE,
        related_name="monthly_cards"
    )

    month = models.CharField(max_length=20)
    cards_count = models.BigIntegerField()


from django.db import models


class BranchDashboardReport(models.Model):
    total_cards = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class BranchDashboardItem(models.Model):
    report = models.ForeignKey(
        BranchDashboardReport,
        on_delete=models.CASCADE,
        related_name="branches"
    )

    head_office = models.CharField(max_length=255)
    total_cards = models.BigIntegerField()
    active_cards = models.BigIntegerField()
    active_percentage = models.DecimalField(max_digits=10, decimal_places=2)


class BranchCardTypeStat(models.Model):
    branch = models.ForeignKey(
        BranchDashboardItem,
        on_delete=models.CASCADE,
        related_name="card_types"
    )

    card_type = models.CharField(max_length=50)
    total = models.BigIntegerField()
    active = models.BigIntegerField()


class BranchBalance(models.Model):
    branch = models.OneToOneField(
        BranchDashboardItem,
        on_delete=models.CASCADE,
        related_name="balances"
    )

    uzs = models.DecimalField(max_digits=30, decimal_places=2)
    usd = models.DecimalField(max_digits=30, decimal_places=2)


class BranchDormantStat(models.Model):
    branch = models.OneToOneField(
        BranchDashboardItem,
        on_delete=models.CASCADE,
        related_name="dormant"
    )

    count = models.BigIntegerField()
    percentage = models.DecimalField(max_digits=10, decimal_places=2)
    uzs_cards = models.BigIntegerField()
    usd_cards = models.BigIntegerField()