from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework import permissions, viewsets

from invoicing.models import Customer, Invoice, Supplier
from invoicing.serializers import (
    InvoiceSerializer,
    CustomerSerializer,
    UserSerializer,
    GroupSerializer,
)
from invoicing.serializers.invoicing_serializers import SupplierSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be viewed or edited.
    """

    queryset = Customer.objects.all().order_by("name")
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows suppliers to be viewed or edited.
    """

    queryset = Supplier.objects.all().order_by("user")
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows invoices to be viewed or edited.
    """

    queryset = Invoice.objects.all().order_by("-date")
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
