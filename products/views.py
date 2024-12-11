from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import PRODUCTS_NOT_FOUND_MSG, DISCOUNT_NOT_FOUND_MSG, ORDER_NOT_FOUND_MSG, PRODUCTS_LIST_SUCCESS_MSG, \
    PRODUCT_CREATED_SUCCESS_MSG, PRODUCT_UPDATED_SUCCESS_MSG, PRODUCT_DELETED_SUCCESS_MSG, DISCOUNT_CREATED_SUCCESS_MSG, \
    DISCOUNT_LIST_SUCCESS_MSG, DISCOUNT_UPDATED_SUCCESS_MSG, DISCOUNT_DELETED_SUCCESS_MSG, ORDER_CREATED_SUCCESS_MSG, \
    ORDER_RETRIEVED_SUCCESS_MSG, ORDER_UPDATED_SUCCESS_MSG, ORDER_DELETED_SUCCESS_MSG
from .models import Product, Discount, Order
from .serializers import ProductSerializer, DiscountSerializer, OrderSerializer
from .utils import response_converter


# Product Views
class ProductListCreateAPIView(APIView):
    """
    view for the products.here we add, created and get the products.
    """
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(response_converter(True, PRODUCTS_LIST_SUCCESS_MSG, serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_converter(True, PRODUCT_CREATED_SUCCESS_MSG, serializer.data), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    """
    view for the retrieve, update and delete the products.
    """
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(response_converter(False, PRODUCTS_NOT_FOUND_MSG, None),
                     status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(response_converter(True, PRODUCTS_LIST_SUCCESS_MSG, serializer.data), status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(response_converter(False, PRODUCTS_NOT_FOUND_MSG, None),
                            status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_converter(True, PRODUCT_UPDATED_SUCCESS_MSG, serializer.data), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(response_converter(False, PRODUCTS_NOT_FOUND_MSG, None),
                            status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(response_converter(True, PRODUCT_DELETED_SUCCESS_MSG, None),
                        status=status.HTTP_204_NO_CONTENT)


class DiscountListCreateAPIView(APIView):
    """
    view for the discount create and list.
    """
    def get(self, request):
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return Response(response_converter(True, DISCOUNT_LIST_SUCCESS_MSG, serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                response_converter(True, DISCOUNT_CREATED_SUCCESS_MSG, serializer.data),
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiscountDetailAPIView(APIView):
    """
    discount retrieve, update and delete.
    """
    def get_object(self, pk):
        try:
            return Discount.objects.get(pk=pk)
        except Discount.DoesNotExist:
            return None

    def get(self, request, pk):
        discount = self.get_object(pk)
        if not discount:
            return Response({"error": DISCOUNT_NOT_FOUND_MSG}, status=status.HTTP_404_NOT_FOUND)
        serializer = DiscountSerializer(discount)
        return Response(response_converter(True, DISCOUNT_LIST_SUCCESS_MSG, serializer.data), status=status.HTTP_200_OK)

    def put(self, request, pk):
        discount = self.get_object(pk)
        if not discount:
            return Response({"error": DISCOUNT_NOT_FOUND_MSG}, status=status.HTTP_404_NOT_FOUND)
        serializer = DiscountSerializer(discount, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                response_converter(True, DISCOUNT_UPDATED_SUCCESS_MSG, serializer.data),
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        discount = self.get_object(pk)
        if not discount:
            return Response({"error": DISCOUNT_NOT_FOUND_MSG}, status=status.HTTP_404_NOT_FOUND)
        discount.delete()
        return Response(
            response_converter(True, DISCOUNT_DELETED_SUCCESS_MSG, None),
            status=status.HTTP_204_NO_CONTENT
        )


class OrderListCreateAPIView(APIView):
    """
    view for the order create and lists.
    """
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                response_converter(True, ORDER_CREATED_SUCCESS_MSG, serializer.data),
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    """
    view for the order retrieve, update and delete.
    """
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response({"error": ORDER_NOT_FOUND_MSG}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(
            response_converter(True, ORDER_RETRIEVED_SUCCESS_MSG, serializer.data),
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response({"error": ORDER_NOT_FOUND_MSG}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                response_converter(True, ORDER_UPDATED_SUCCESS_MSG, serializer.data),
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response({"error": ORDER_NOT_FOUND_MSG}, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(
                response_converter(True, ORDER_DELETED_SUCCESS_MSG, None),
                status=status.HTTP_204_NO_CONTENT
            )

