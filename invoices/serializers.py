from rest_framework import serializers
from .models import Invoice, InvoiceDetail


class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = ['description', 'quantity', 'price', 'line_total']


class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['invoice_number', 'customer_name', 'date', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        invoice = Invoice.objects.create(**validated_data)
        for detail_data in details_data:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)
        return invoice

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        details_data = validated_data.get('details', None)
        if details_data is not None:
            instance.details.all().delete()
            for detail_data in details_data:
                InvoiceDetail.objects.create(invoice=instance, **detail_data)

        return instance
