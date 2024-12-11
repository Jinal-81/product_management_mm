from rest_framework import serializers
from .models import Product, Discount, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'order']
        extra_kwargs = {'order': {'required': False, 'write_only': True}}


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    discounts = serializers.PrimaryKeyRelatedField(many=True, queryset=Discount.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'items', 'discounts', 'total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        discounts_data = validated_data.pop('discounts')

        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            item_data['order'] = order
            OrderItem.objects.create(**item_data)

        for discount_id in discounts_data:
            discount = Discount.objects.get(id=discount_id.id)
            order.discounts.add(discount)

        order.calculate_total()

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        discounts_data = validated_data.pop('discounts', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)

        if discounts_data is not None:
            instance.discounts.set(discounts_data)

        instance.calculate_total()
        instance.save()
        return instance
