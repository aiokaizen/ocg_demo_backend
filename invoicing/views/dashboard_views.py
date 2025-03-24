from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncMonth
from django.db.models import Avg, Sum, Count

from invoicing.models import Customer, Invoice
from rest_framework.views import APIView, Response, status

User = get_user_model()


class Dashboard(APIView):
    def get(self, *args, **kwargs):
        """
        Collect some metrics for the dashboard.
        """

        # Get all-time stats
        alltime_stats = Invoice.objects.aggregate(
            count=Count("id"),
            total_amount=Sum("amount"),
        )
        alltime_stats = {
            "count": alltime_stats["count"],
            "sum": alltime_stats["total_amount"],
        }

        # Get invoice stats per month
        invoice_stats = (
            Invoice.objects.annotate(month=TruncMonth("date"))
            .values("month")
            .annotate(
                count=Count("id"), total_amount=Sum("amount"), average=Avg("amount")
            )
            .order_by("month")
        )
        monthly_invoice_stats = {}
        for stat in invoice_stats:
            stats = {
                "count": stat["count"],
                "sum": stat["total_amount"],
                "avg": stat["average"],
            }
            monthly_invoice_stats[stat["month"].strftime("%m-%Y")] = stats

        data = {
            "monthly_invoice_stats": monthly_invoice_stats,
            "alltime_stats": alltime_stats,
        }
        return Response(data, status.HTTP_200_OK)
