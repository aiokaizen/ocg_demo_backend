from rest_framework import serializers

from invoicing.models import Customer, Invoice


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ["url", "user", "name", "email", "image"]


class CustomerListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ["url", "name", "email", "image"]


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invoice
        fields = ["url", "customer", "amount", "date", "status"]

    def create(self, validated_data):
        """
        Create and return a new `Invoice` instance, given the validated data.
        """
        return Invoice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Invoice` instance, given the validated data.
        """
        # Generic solution
        # for k, v in validated_data.items():
        #     if hasattr(instance, k) and v:
        #         setattr(instance, k)

        instance.customer = validated_data.get("customer", instance.customer)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.date = validated_data.get("date", instance.date)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


class InvoiceListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invoice
        fields = ["url", "customer", "amount", "date", "status"]
