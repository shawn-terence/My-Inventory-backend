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