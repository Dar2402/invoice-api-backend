from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Invoice
from .serializers import InvoiceSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.


class InvoiceAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Create a new invoice along with multiple invoice details.",
        request_body=InvoiceSerializer,
        responses={
            status.HTTP_201_CREATED: InvoiceSerializer,
            status.HTTP_400_BAD_REQUEST: "Invalid data"
        },
        request_body_examples={
            "application/json": {
                "invoice_number": "INV001",
                "customer_name": "John Doe",
                "date": "2024-11-12",
                "details": [
                    {
                        "description": "Product A",
                        "quantity": 2,
                        "price": 50.00,
                        "line_total": 100.00
                    },
                    {
                        "description": "Product B",
                        "quantity": 1,
                        "price": 75.00,
                        "line_total": 75.00
                    }
                ]
            }
        }
    )
    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update an existing invoice and its details.",
        request_body=InvoiceSerializer,
        responses={
            status.HTTP_200_OK: InvoiceSerializer,
            status.HTTP_400_BAD_REQUEST: "Invalid data",
            status.HTTP_404_NOT_FOUND: "Invoice not found"
        }
    )
    def put(self, request):
        invoice_number = request.data.get('invoice_number')

        if not invoice_number:
            return Response({"error": "invoice_number is required for updates."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invoice = Invoice.objects.get(invoice_number=invoice_number)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InvoiceSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update an existing invoice and its details.",
        request_body=InvoiceSerializer,
        responses={
            status.HTTP_200_OK: InvoiceSerializer,
            status.HTTP_400_BAD_REQUEST: "Invalid data",
            status.HTTP_404_NOT_FOUND: "Invoice not found"
        }
    )
    def patch(self, request):
        invoice_number = request.data.get('invoice_number')

        if not invoice_number:
            return Response({"error": "invoice_number is required for updates."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invoice = Invoice.objects.get(invoice_number=invoice_number)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InvoiceSerializer(
            invoice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
