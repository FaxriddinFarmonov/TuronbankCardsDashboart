from django.db import models


class ActiveCard(models.Model):
    branch_code = models.CharField(max_length=50)  # 1
    branch_name = models.CharField(max_length=255)  # 2
    parent_branch = models.CharField(max_length=50, null=True, blank=True)  # 3
    level = models.CharField(max_length=20, null=True, blank=True)  # 4
    account = models.CharField(max_length=100)  # 5

    dt_turnover = models.DateField(null=True, blank=True)
    ct_turnover = models.DateField(null=True, blank=True)
    client_type = models.CharField(max_length=100)  # 8
    card_type = models.CharField(max_length=100)  # 9

    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # 10
    balance_equivalent = models.DecimalField(max_digits=20, decimal_places=2, default=0)  # 11

    doc_date = models.DateField(null=True, blank=True)  # 12
    expire_date = models.DateField(null=True, blank=True)  # 13

    card_system = models.CharField(max_length=50)  # 14
    card_status = models.CharField(max_length=100)  # 15

    currency_code = models.CharField(max_length=10)  # 16
    # HEAD OFFICE

    head_office = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # ID BANK
    id_bank = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    resident_status = models.CharField(max_length=10)  # 17
    client_full_name = models.CharField(max_length=255)  # 18

    row_number = models.IntegerField()  # 19 (№ p/п)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "active_cards"
        indexes = [
            models.Index(fields=["account"]),
            models.Index(fields=["branch_code"]),
        ]

    # ====== 19 ta helper method (sening talabingga mos) ======
    def is_resident(self):
        return self.resident_status == "1"

    def is_active(self):
        return self.card_status == "Карта выпущена"

    def short_name(self):
        return self.client_full_name[:30]