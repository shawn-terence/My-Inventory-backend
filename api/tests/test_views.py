from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import Inventory, Transaction
from datetime import datetime, date

User = get_user_model()

class UserRegistrationTest(APITestCase):
    def test_user_registration(self):
        url = '/register/'
        data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'employee',
            'password': 'securepassword123',
        }
        response = self.client.post(url, data, format='json')
        if response.status_code == status.HTTP_201_CREATED:
            print("User registration test passed")
        else:
            print("User registration test failed")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

class UserLoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            role='employee',
            password='securepassword123'
        )
    
    def test_user_login(self):
        url = '/login/'
        data = {
            'email': 'testuser@example.com',
            'password': 'securepassword123',
        }
        response = self.client.post(url, data, format='json')
        if response.status_code == status.HTTP_200_OK:
            print("User login test passed")
        else:
            print("User login test failed")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class AddInventoryTest(APITestCase):
    def test_add_inventory(self):
        url = '/inventory/add/'
        data = {
            'name': 'Test Item',
            'description': 'Description of Test Item',
            'price': '9.99',
            'quantity': 100
        }
        response = self.client.post(url, data, format='json')
        if response.status_code == status.HTTP_201_CREATED:
            print("Add inventory test passed")
        else:
            print("Add inventory test failed")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Item')

class InventoryListTest(APITestCase):
    def setUp(self):
        self.inventory_item = Inventory.objects.create(
            name='Test Item',
            description='Description of Test Item',
            price='9.99',
            quantity=100
        )
    
    def test_get_inventory_list(self):
        url = '/inventory/'
        response = self.client.get(url)
        if response.status_code == status.HTTP_200_OK:
            print("Inventory list test passed")
        else:
            print("Inventory list test failed")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Item')

class UpdateInventoryTest(APITestCase):
    def setUp(self):
        self.inventory_item = Inventory.objects.create(
            name='Test Item',
            description='Description of Test Item',
            price='9.99',
            quantity=100
        )
    
    def test_update_inventory(self):
        url = f'/update/{self.inventory_item.id}/add/'
        data = {'quantity': 50}
        response = self.client.put(url, data, format='json')
        if response.status_code == status.HTTP_200_OK:
            print("Update inventory test passed")
        else:
            print("Update inventory test failed")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventory_item.refresh_from_db()
        self.assertEqual(self.inventory_item.quantity, 150)

class DeleteInventoryTest(APITestCase):
    def setUp(self):
        self.inventory_item = Inventory.objects.create(
            name='Test Item',
            description='Description of Test Item',
            price='9.99',
            quantity=100
        )
    
    def test_delete_inventory(self):
        url = f'/inventory/{self.inventory_item.id}/delete'
        response = self.client.delete(url)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            print("Delete inventory test passed")
        else:
            print("Delete inventory test failed")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Inventory.objects.count(), 0)

class TransactionsListTest(APITestCase):
    def setUp(self):
        self.inventory_item = Inventory.objects.create(
            name='Test Item',
            description='Description of Test Item',
            price='9.99',
            quantity=100
        )
        self.transaction = Transaction.objects.create(
            inventory=self.inventory_item,
            product_name=self.inventory_item.name,
            date=date.today(),
            time=datetime.now().time()
        )
    
    def test_get_transactions(self):
        url = '/transactions/'
        response = self.client.get(url)
        if response.status_code == status.HTTP_200_OK:
            print("Transactions list test passed")
        else:
            print("Transactions list test failed")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['product_name'], 'Test Item')

class PurchaseTest(APITestCase):
    def setUp(self):
        self.inventory_item = Inventory.objects.create(
            name='Test Item',
            description='Description of Test Item',
            price='9.99',
            quantity=100
        )
        self.user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            role='employee',
            password='securepassword123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_purchase(self):
        url = '/purchase/'
        data = {
            'items': [
                {'id': self.inventory_item.id, 'quantity': 1}
            ]
        }
        response = self.client.post(url, data, format='json')
        if response.status_code == status.HTTP_200_OK:
            print("Purchase test passed")
        else:
            print("Purchase test failed")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventory_item.refresh_from_db()
        self.assertEqual(self.inventory_item.quantity, 99)
