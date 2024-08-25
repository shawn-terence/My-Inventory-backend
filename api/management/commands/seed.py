# api/management/commands/seed.py

from django.core.management.base import BaseCommand
from api.models import Inventory, Transaction
from django.contrib.auth import get_user_model
from datetime import datetime
import random

class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Clear existing data
        self.stdout.write(self.style.WARNING("Clearing existing data..."))
        
        # Clear users except superusers
        User.objects.exclude(is_superuser=True).delete()
        self.stdout.write(self.style.SUCCESS("Users cleared."))
        
        # Clear inventory and transactions
        Inventory.objects.all().delete()
        Transaction.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Inventory and transactions cleared."))

        # Create a user
        user, created = User.objects.get_or_create(
            email="seeduser@example.com",
            defaults={
                'first_name': "Seed",
                'last_name': "User",
                'role': 'employee',
                'password': 'securepassword123',
            }
        )
        if created:
            user.set_password('securepassword123')
            user.save()
        self.stdout.write(self.style.SUCCESS(f"User created: {user.email}"))

        # Create inventory items for a tech store
        tech_items = [
            ("Laptop", "High-performance laptop suitable for gaming and work", 999),
            ("Desktop PC", "Powerful desktop computer for office and gaming", 1299),
            ("Hard Drive", "1TB external hard drive", 59),
            ("SSD", "500GB SSD for faster storage", 89),
            ("Monitor", "27-inch 4K monitor", 399),
            ("Keyboard", "Mechanical keyboard with backlight", 79),
            ("Mouse", "Wireless ergonomic mouse", 49),
            ("Printer", "All-in-one color printer", 199),
            ("Headphones", "Noise-cancelling over-ear headphones", 149),
            ("Webcam", "HD webcam for video conferencing", 89),
            ("Router", "Dual-band Wi-Fi router", 129),
            ("Microphone", "USB microphone for podcasting", 119),
            ("Docking Station", "USB-C docking station for laptops", 139),
            ("Graphics Card", "NVIDIA GeForce GTX 1660", 229),
            ("USB Hub", "7-port USB 3.0 hub", 29),
            ("Surge Protector", "12-outlet surge protector", 49),
            ("UPS", "Uninterruptible power supply", 159),
            ("External Battery", "Portable external battery pack", 39),
            ("Tablet", "10-inch Android tablet", 249),
            ("Smartwatch", "Fitness smartwatch with GPS", 199),
        ]

        inventory_items = []
        for name, description, price in tech_items:
            item = Inventory.objects.create(
                name=name,
                description=description,
                price=price,
                quantity=50  # Default quantity
            )
            inventory_items.append(item)
        self.stdout.write(self.style.SUCCESS(f"{len(inventory_items)} inventory items created."))

        # Create transactions
        for i in range(100):  # Create 100 transactions
            item = random.choice(inventory_items)
            Transaction.objects.create(
                inventory=item,
                product_name=item.name,
                date=datetime.now().date(),
                time=datetime.now().time()
            )
        self.stdout.write(self.style.SUCCESS("Transactions created."))

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database"))
