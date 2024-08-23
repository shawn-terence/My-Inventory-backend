from django.shortcuts import render
from .models import *
from .serializers import *
from django.db import transaction
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .forms import UploadFileForm
from django.db import transaction as db_transaction
from datetime import datetime
import pandas as pd

# Create your views here.
User=get_user_model()

#User registration 
class UserRegistrationView(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#User login view
class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user=user)
                
            response_data = {
                'message': 'Log in successful',
                'token': token.key
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid email and/or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

 
"""                                                     INVENTORY VIEWS                                                                             """
#Add inventory
class AddInventoryView(APIView):
    def post(self,request):
        serializer=InventorySerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#Upload inventory using spreadsheet
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_file_view(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']
    try:
        df = pd.read_excel(file)  # Read the spreadsheet into a DataFrame
    except Exception as e:
        return JsonResponse({'error': f'Invalid file format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    # Rename the columns
    expected_columns = ['name', 'description', 'price', 'quantity']
    if not all(column in df.columns for column in expected_columns):
        return JsonResponse({'error': f'File must contain the following columns: {expected_columns}'}, status=status.HTTP_400_BAD_REQUEST)

    df = df[expected_columns]  # Ensure the DataFrame only contains the expected columns

    for index, row in df.iterrows():
        Inventory.objects.create(
            name=row['name'],
            description=row['description'],
            price=row['price'],
            quantity=row['quantity']
        )

    return JsonResponse({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
#Get inventory list
class InventoryListView(APIView):
    def get(self,request):
        inventory=Inventory.objects.all()
        serializer=InventorySerializer(inventory,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

#update Inventory
class UpdateInventoryView(APIView):
    def put(self, request, pk):
        try:
            inventory = Inventory.objects.get(id=pk)
        except Inventory.DoesNotExist:
            return Response({"message": "Inventory item not found"}, status=status.HTTP_404_NOT_FOUND)

        added_quantity = request.data.get("quantity")
        if isinstance(added_quantity, int) and added_quantity > 0:
            inventory.quantity += added_quantity
            inventory.save()
            return Response({"message": "Inventory updated successfully"}, status=status.HTTP_200_OK)

        return Response({"message": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
#Delete Item
class DeleteInventoryView(APIView):
    def delete(self,request,pk):
        inventory=Inventory.objects.get(id=pk)
        inventory.delete()
        return Response({"message":"Inventory deleted successfully"},status=status.HTTP_204_NO_CONTENT)


"""                                                 Transaction Views                                                                   """
#Get transactions
class TransactionsView(APIView):
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)