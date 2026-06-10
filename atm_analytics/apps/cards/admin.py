from django.contrib.admin import SimpleListFilter
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from django import forms
from django.db.models import Q
from rangefilter.filters import DateRangeFilter
import tempfile
import os
from django.db.models import Count
import json
from .models import ActiveCard
from .services import import_excel


# =========================================================
# EXCEL UPLOAD FORM
# =========================================================
class ExcelUploadForm(forms.Form):

    file = forms.FileField(
        label="Excel fayl yuklang",
        help_text=".xlsx formatdagi faylni tanlang"
    )


# =========================================================
# =====================================================
# CARD TYPE FILTER
# =====================================================
class CardTypeFilter(SimpleListFilter):

    title = "CARD TYPE"

    parameter_name = "card_type_custom"

    # =================================================
    # FILTER LIST
    # =================================================
    def lookups(self, request, model_admin):

        return (

            ("HUMO", "HUMO"),

            ("MASTER", "MASTER CARD"),

            ("UZCARD", "UZCARD"),

            ("VISA", "VISA"),
        )

    # =================================================
    # FILTER QUERY
    # =================================================
    def queryset(self, request, queryset):

        value = self.value()

        # =============================================
        # HUMO
        # =============================================
        if value == "HUMO":

            return queryset.filter(
                card_system="HUMO1"
            )

        # =============================================
        # MASTER CARD
        # =============================================
        if value == "MASTER":

            return queryset.filter(
                card_system__in=[

                    "MC GL TURN",

                    "MC GLD TUR",

                    "MC GOLD",

                    "MC ST VI",

                    "MC Standar",


                ]
            )

        # =============================================
        # UZCARD
        # =============================================
        if value == "UZCARD":

            return queryset.filter(
                card_system__in=[

                    "UZBCBJDUO",

                    "UZCARD",
                    "MIR",
                ]
            )

        # =============================================
        # VISA
        # =============================================
        if value == "VISA":

            return queryset.filter(
                card_system__in=[

                    "VISA BSN",

                    "VISA CL DT",

                    "VISA CL EX",

                    "VISA CL VI",

                    "VISA GDE",

                    "VISA GOLD",
                ]
            )

        return queryset

# ADMIN
# =========================================================
@admin.register(ActiveCard)
class ActiveCardAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):

        response = super().changelist_view(request, extra_context=extra_context)

        try:
            cl = response.context_data.get("cl")

            if not cl:
                return response

            qs = cl.queryset

            # =========================
            # CARD SYSTEM (REAL DATA FIX)
            # =========================
            card_types = list(
                qs.values("card_system")
                .annotate(total=Count("id"))
                .order_by("-total")
            )

            # =========================
            # STATUS
            # =========================
            status_data = list(
                qs.values("card_status")
                .annotate(total=Count("id"))
                .order_by("-total")
            )

            response.context_data["total_cards"] = qs.count()
            response.context_data["card_type_chart"] = json.dumps(card_types, ensure_ascii=False)
            response.context_data["status_chart"] = json.dumps(status_data, ensure_ascii=False)

        except Exception as e:
            print("ADMIN DASHBOARD ERROR:", e)

        return response
    # =====================================================
    # CUSTOM TEMPLATE
    # =====================================================
    change_list_template = "admin/cards/activecard/change_list.html"

    # =====================================================
    # TABLE COLUMNS
    # =====================================================
    list_display = (

        "branch_code",
        "id_bank",
        "head_office",

        "branch_name",

        "account",

        "client_full_name",

        "client_type",

        "card_type",
        "card_system",

        "currency_code",

        "balance",
        "balance_equivalent",

        "dt_turnover",
        "ct_turnover",

        "card_status",

        "resident_badge",

        "doc_date",
        "expire_date",
    )

    # =====================================================
    # CLICKABLE COLUMN
    # =====================================================
    list_display_links = (
        "account",
        "client_full_name",
    )

    # =====================================================
    # SEARCH
    # =====================================================
    search_fields = (

        "account",

        "client_full_name",

        "branch_code",

        "id_bank",

        "head_office",

        "branch_name",

        "card_type",

        "card_system",

        "currency_code",

        "card_status",
    )

    # =====================================================
    # FILTERS
    # =====================================================


    list_filter = (
        CardTypeFilter,

        ("doc_date", DateRangeFilter),

        "head_office",

        "id_bank",

        "card_status",

        "currency_code",

        "card_system",

        "resident_status",

        "client_type",
    )
    # =====================================================
    # SORT
    # =====================================================
    ordering = (
        "-id",
    )
    date_hierarchy = "doc_date"
    # =====================================================
    # PAGINATION
    # =====================================================
    list_per_page = 20

    # =====================================================
    # PERFORMANCE
    # =====================================================
    show_full_result_count = False

    # =====================================================
    # READ ONLY
    # =====================================================
    readonly_fields = (
        "created_at",
    )

    # =====================================================
    # =====================================================
    # ACTIONS
    # =====================================================
    actions = ["delete_all_records"]
    # SEARCH OPTIMIZATION
    # =====================================================
    def get_search_results(
        self,
        request,
        queryset,
        search_term
    ):

        queryset, use_distinct = super().get_search_results(
            request,
            queryset,
            search_term
        )

        if search_term:

            queryset |= self.model.objects.filter(

                Q(account__icontains=search_term) |

                Q(client_full_name__icontains=search_term) |

                Q(branch_name__icontains=search_term) |

                Q(branch_code__icontains=search_term) |

                Q(id_bank__icontains=search_term) |

                Q(head_office__icontains=search_term)
            )

        return queryset, use_distinct

    # =====================================================
    # RESIDENT BADGE
    # =====================================================
    @admin.display(description="Rezident")
    def resident_badge(self, obj):

        if obj.resident_status == "1":
            return "✅ Rezident"

        return "❌ Nerezident"

    # =====================================================

    # =====================================================
    # DELETE ALL
    # =====================================================
    @admin.action(description="🗑 DELETE ALL DATA")
    def delete_all_records(self, request, queryset):

        total = ActiveCard.objects.count()

        ActiveCard.objects.all().delete()

        self.message_user(

            request,

            f"""
            ✅ Barcha ma'lumotlar o‘chirildi.

            O‘chirilgan rowlar soni: {total}
            """,

            level=messages.SUCCESS
        )

    # FIELDSETS
    # =====================================================
    fieldsets = (

        # =================================================
        # FILIAL
        # =================================================
        ("Filial ma'lumotlari", {

            "fields": (

                "row_number",

                "branch_code",

                "id_bank",

                "head_office",

                "branch_name",

                "parent_branch",

                "level",
            )
        }),

        # =================================================
        # HISOB
        # =================================================
        ("Hisob ma'lumotlari", {

            "fields": (

                "account",

                "client_type",

                "client_full_name",

                "resident_status",
            )
        }),

        # =================================================
        # KARTA
        # =================================================
        ("Karta ma'lumotlari", {

            "fields": (

                "card_type",

                "card_system",

                "card_status",

                "currency_code",
            )
        }),

        # =================================================
        # BALANCE
        # =================================================
        ("Balans va оборот", {

            "fields": (

                "balance",

                "balance_equivalent",

                "dt_turnover",

                "ct_turnover",
            )
        }),

        # =================================================
        # SANALAR
        # =================================================
        ("Sana ma'lumotlari", {

            "fields": (

                "doc_date",

                "expire_date",

                "created_at",
            )
        }),

    )
    # =====================================================
    # URLS
    # =====================================================
    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [

            path(
                "upload-excel/",
                self.admin_site.admin_view(
                    self.upload_excel
                ),
                name="activecard_upload_excel",
            ),
        ]

        return custom_urls + urls

    # =====================================================
    # EXCEL IMPORT
    # =====================================================
    def upload_excel(self, request):

        if request.method == "POST":

            form = ExcelUploadForm(
                request.POST,
                request.FILES
            )

            if form.is_valid():

                uploaded_file = request.FILES["file"]

                # =============================================
                # TEMP FILE
                # =============================================
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".xlsx"
                )

                try:

                    # =========================================
                    # SAVE TEMP FILE
                    # =========================================
                    for chunk in uploaded_file.chunks():

                        temp_file.write(chunk)

                    temp_file.close()

                    # =========================================
                    # IMPORT EXCEL
                    # =========================================
                    result = import_excel(
                        temp_file.name
                    )

                    # =========================================
                    # SUCCESS MESSAGE
                    # =========================================
                    messages.success(
                        request,
                        f"""
                        ✅ Excel muvaffaqiyatli yuklandi.

                        Yuklangan: {result['success']}

                        Xatolar: {result['errors']}
                        """
                    )

                    return redirect("../")

                except Exception as e:

                    messages.error(
                        request,
                        f"""
                        ❌ Import xatoligi:

                        {str(e)}
                        """
                    )

                finally:

                    # =========================================
                    # DELETE TEMP FILE
                    # =========================================
                    if os.path.exists(temp_file.name):

                        os.unlink(temp_file.name)

        else:

            form = ExcelUploadForm()

        # =================================================
        # RENDER PAGE
        # =================================================
        return render(

            request,

            "admin/excel_upload.html",

            {
                "form": form,
                "title": "Excel import qilish"
            }
        )