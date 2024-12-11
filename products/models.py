from django.db import models


class Product(models.Model):
    """
    model for products.
    """
    name = models.CharField(max_length=100)
    base_price = models.FloatField()

    def get_price(self, quantity=1):
        """
        method for the price, which return the price based on quantity and base price.
        """
        return self.base_price * quantity

    def __str__(self):
        return self.name


class SeasonalProduct(Product):
    """
    model for the seasonal products.
    """
    season_discount = models.FloatField(default=0.0)

    def get_price(self, quantity=1):
        """
        method for the price which return the price base on season discount and parent class's get price method.
        (which return the price base on quantity and price)
        """
        return super().get_price(quantity) * (1 - self.season_discount)


class BulkProduct(Product):
    """
    model for the bulk products.
    """
    def get_price(self, quantity=1):
        """
        method returns the price according different quantities and apply the discount accordingly.this one also
        inherit the parent class get price method.
        """
        if 10 <= quantity <= 20:
            discount = 0.05
        elif 21 <= quantity <= 50:
            discount = 0.10
        elif quantity > 50:
            discount = 0.15
        else:
            discount = 0
        return super().get_price(quantity) * (1 - discount)


class PremiumProduct(Product):
    """
    model for the premium products which also derived product class.
    """
    markup = models.FloatField(default=0.15)

    def get_price(self, quantity=1):
        """
        method return the price according quantity and markup.
        """
        return super().get_price(quantity) * (1 + self.markup)


class Discount(models.Model):
    """
    model for the discounts.
    """
    name = models.CharField(max_length=100)
    priority = models.IntegerField()

    def apply_discount(self, price):
        """
        method return the price.
        """
        return price

    def __str__(self):
        return self.name


class PercentageDiscount(Discount):
    """
    model for the percentage discount.
    """
    percentage = models.FloatField()

    def apply_discount(self, price):
        """
        method return the price according percentage discount.
        """
        return price * (1 - self.percentage)


class FixedAmountDiscount(Discount):
    """
    model for the fixed amount.
    """
    amount = models.FloatField()

    def apply_discount(self, price):
        """
        return the discount according price and amount.
        """
        return max(price - self.amount, 0)


class TieredDiscount(Discount):
    """
    model for the tiered discount.
    """
    tiers = models.JSONField()  # e.g., {"500": 0.05, "1000": 0.10}

    def apply_discount(self, price):
        """
        method return the discount on tiers items and return the price.
        """
        for threshold, discount in sorted(self.tiers.items(), reverse=True):
            if price > float(threshold):
                return price * (1 - discount)
        return price


class Order(models.Model):
    """
    model for the orders.
    """
    products = models.ManyToManyField(Product, through='OrderItem')
    discounts = models.ManyToManyField(Discount)
    total_price = models.FloatField(default=0.0, editable=False)

    def calculate_total(self):
        """
        method returns the total price according items, price and discount applied values.
        """
        total = sum(item.product.get_price(item.quantity) for item in self.items.all())
        self.discounts.all().order_by('priority')
        for discount in self.discounts.all():
            total = discount.apply_discount(total)
        self.total_price = total
        self.save()
        return self.total_price


class OrderItem(models.Model):
    """
    model for the order items.
    """
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

