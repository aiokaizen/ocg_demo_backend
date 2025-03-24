from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from pylibutils.utils import naive_utcnow

from invoicing.settings import INVOICE_STATUS_CHOICES

User = get_user_model()


class Customer(models.Model):
    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    user = models.ForeignKey(
        User, verbose_name=_("User"), on_delete=models.PROTECT, null=True, blank=True
    )
    name = models.CharField(_("Name"), max_length=128)
    email = models.CharField(_("Email"), max_length=128)
    image = models.ImageField(_("Image URL"), null=True, blank=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
        ordering = ["-date"]

    customer = models.ForeignKey(
        Customer,
        verbose_name=_("Customer"),
        on_delete=models.PROTECT,
        related_name="invoices",
    )
    amount = models.DecimalField(_("Amount"), decimal_places=2, max_digits=11)
    date = models.DateTimeField(_("Invoice date"), default=naive_utcnow, blank=True)
    status = models.CharField(
        _("Status"), choices=INVOICE_STATUS_CHOICES, default="pending", max_length=32
    )

    def __str__(self):
        return f"{self.status} | {self.amount} {self.customer}"
