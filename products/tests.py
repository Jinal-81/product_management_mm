from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product, Discount, Order, OrderItem, PercentageDiscount, FixedAmountDiscount


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", base_price=100.0)

    def test_get_price(self):
        self.assertEqual(self.product.get_price(2), 200.0)


class DiscountModelTestCase(TestCase):
    def setUp(self):
        self.discount = PercentageDiscount.objects.create(name="10% Off", priority=1, percentage=0.1)

    def test_apply_discount(self):
        discounted_price = self.discount.apply_discount(100.0)
        self.assertEqual(discounted_price, 90.0)


class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_data = {"name": "Test Product", "base_price": 100.0}
        self.product = Product.objects.create(**self.product_data)

    def test_list_products(self):
        response = self.client.get("/products/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

    def test_create_product(self):
        data = {"name": "New Product", "base_price": 200.0}
        response = self.client.post("/products/products/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["name"], "New Product")

    def test_update_product(self):
        updated_data = {"name": "Updated Product", "base_price": 150.0}
        response = self.client.put(f"/products/products/{self.product.id}/", updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["name"], "Updated Product")

    def test_delete_product(self):
        response = self.client.delete(f"/products/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class DiscountAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.discount_data = {"name": "10% Off", "priority": 1, "percentage": 0.1}
        self.discount = PercentageDiscount.objects.create(**self.discount_data)

    def test_list_discounts(self):
        response = self.client.get("/products/discounts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

    def test_create_discount(self):
        data = {"name": "$10 Off", "priority": 2, "amount": 10.0, "type": "fixed"}
        response = self.client.post("/products/discounts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["name"], "$10 Off")

    def test_update_discount(self):
        updated_data = {"name": "15% Off", "priority": 1, "percentage": 0.15}
        response = self.client.put(f"/products/discounts/{self.discount.id}/", updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["name"], "15% Off")

    def test_delete_discount(self):
        response = self.client.delete(f"/products/discounts/{self.discount.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name="Test Product", base_price=100.0)
        self.discount = FixedAmountDiscount.objects.create(name="$10 Off", priority=1, amount=10.0)

        self.order_data = {
            "items": [
                {"product": self.product.id, "quantity": 2}  # No need to include `order` here
            ],
            "discounts": [self.discount.id]
        }
        self.order = Order.objects.create()
        OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        self.order.discounts.add(self.discount)

    def test_list_orders(self):
        response = self.client.get("/products/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_order(self):
        response = self.client.post("/products/orders/", self.order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("total_price", response.data["data"])  # Check if the total price is calculated and returned

    def test_update_order(self):
        # Get the current items from the existing order to keep them intact during the update
        items_data = [{'product': item.product.id, 'quantity': item.quantity} for item in self.order.items.all()]

        updated_data = {
            "items": items_data,  # Include the existing items
            "discounts": []  # Remove all discounts
        }

        response = self.client.put(f"/products/orders/{self.order.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["total_price"], 200.0)  # No discount applied

    def test_delete_order(self):
        response = self.client.delete(f"/products/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
