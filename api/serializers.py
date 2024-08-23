from rest_framework import serializers
from .models import User,Transaction,Inventory

#user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name','last_name', 'email', 'password','role')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        return user
#Inventory serializer
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'name', 'description', 'quantity', 'price')
    def create(self,validated_data):
        inventory = Inventory.objects.create(**validated_data)
        return inventory
#Transaction serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields=('id','inventory','product_name','date','time')
    def create(self,validated_data):
        transaction=Transaction.objects.create(**validated_data)
        return transaction
#Purchase serializer
class PurchaseItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class PurchaseSerializer(serializers.Serializer):
    items=PurchaseItemSerializer(many=True)

    def validate(self, data):
        items = data['items']
        for item in items:
            try:
                inventory_item = Inventory.objects.get(id=item['id'])
                if inventory_item.quantity < item['quantity']:
                    raise serializers.ValidationError(f"Not enough {inventory_item.name} in stock, only {inventory_item.quantity} left")
            except Inventory.DoesNotExist:
                raise serializers.ValidationError(f"Item with id {item['id']} does not exist")
        return data