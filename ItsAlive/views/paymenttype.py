"""View module for handling requests about payment types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ItsAlive.models import PaymentType, Customer
from datetime import *




class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types
    Arguments:
        serializers
    """
    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'merchant_name')
        depth = 1


class PaymentTypes(ViewSet):
    """Payment types for Bangazon API"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Attraction instance
        """

        new_paymenttype = PaymentType()
        new_paymenttype.merchant_name = request.data["merchant_name"]
        new_paymenttype.save()

        serializer = PaymentTypeSerializer(new_paymenttype, context={'request': request})

        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single payment types

        Returns:
            Response -- JSON serialized payment type instance
        """
        try:
            customer = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a payment types

        Returns:
            Response -- Empty body with 204 status code
        """
        new_paymenttype = PaymentType()
        new_paymenttype.merchant_name = request.data["merchant_name"]
        new_paymenttype.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a payment type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            customer = PaymentType.objects.get(pk=pk)
            customer.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to payment types

        Returns:
            Response -- JSON serialized list of payment types
        """
        paymenttypes = PaymentType.objects.all()

        # Support filtering Products by producttype id
        # customer = Customer.objects.get(user=request.auth.user)
        # if customer is not None:
        #     paymenttypes = paymenttypes.filter(customer=customer)

        serializer = PaymentTypeSerializer(
            paymenttypes, many=True, context={'request': request})
        return Response(serializer.data)
