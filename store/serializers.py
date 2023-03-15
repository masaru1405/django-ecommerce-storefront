from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem

class CollectionSerializer(serializers.ModelSerializer):
   class Meta:
      model = Collection
      fields = ['id', 'title', 'products_count']

   products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
   class Meta:
      model = Product
      fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
  
   unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='price')
   price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
   collection = serializers.HyperlinkedRelatedField(
      queryset = Collection.objects.all(),
      view_name = 'collection-detail'
   )

   def calculate_tax(self, product: Product):
      return product.price * Decimal(1.1)

class ReviewSerializer(serializers.ModelSerializer):
   class Meta:
      model = Review
      fields = ['id', 'date', 'name', 'description', 'product']
   
   def create(self, validated_data):
      product_id = self.context['product_id']
      return Review.objects.create(product_id=product_id, **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
   class Meta:
      model = Product
      fields = ['id', 'title', 'price']

class CartItemSerializer(serializers.ModelSerializer):
   product = SimpleProductSerializer()
   total_price = serializers.SerializerMethodField()

   def get_total_price(self, cart_item:CartItem):
      return cart_item.quantity * cart_item.product.price

   class Meta:
      model = CartItem
      fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
   id = serializers.UUIDField(read_only=True)
   items = CartItemSerializer(many=True)
   total_price = serializers.SerializerMethodField()

   def get_total_price(self, cart):
      return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

   class Meta:
      model = Cart
      fields = ['id', 'items', 'total_price']




