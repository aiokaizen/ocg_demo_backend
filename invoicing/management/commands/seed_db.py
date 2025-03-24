from datetime import datetime, timedelta
import logging
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from faker import Faker

from invoicing.models import Customer, Invoice
from invoicing.settings import INVOICE_STATUS_CHOICES

User = get_user_model()


class Command(BaseCommand):
    help = """
    Seed the database with demo data.
    """

    def handle(self, *args, **options):
        # Create the group 'ADMIN' if it does not exist
        admins_group, admins_created = Group.objects.get_or_create(name="ADMIN")

        # Add all available permissions to group ADMINS
        if admins_created:
            admins_group.permissions.add(
                *Permission.objects.all().values_list("id", flat=True)
            )

        # Create the group 'CUSTOMER' if it does not exist
        customers_group, customers_created = Group.objects.get_or_create(
            name="CUSTOMER"
        )
        if customers_created:
            # Attribute some permissions.
            pass

        # Create the superuser and the admin users if they don't exist
        try:
            User.objects.get(username="superuser")
            logging.warning("superuser already exists!")
        except User.DoesNotExist:
            User.objects.create_superuser(
                username="superuser",
                email="admin@ocg.com",
                first_name="OCG",
                last_name="SuperUser",
                password="admin_pass",
            )
            logging.info("superuser was created successfully!")

        fake = Faker()
        user_count = 100
        firstnames = [fake.first_name() for _ in range(user_count)]
        lastnames = [fake.last_name() for _ in range(user_count)]
        email_providers = [
            ("gmail.com", 100),
            ("outlook.com", 50),
            ("yahoo.com", 20),
            ("protonmail.com", 5),
            ("tutanota.com", 5),
        ]
        email_suffixes = [
            suffix for suffix, weight in email_providers for _ in range(weight)
        ]

        # Create customer users
        error_users = 0
        for i in range(user_count):
            try:
                email_suffix = random.choice(email_suffixes)
                username = f"{firstnames[i][0]}.{lastnames[i].replace(' ', '')}".lower()
                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@{email_suffix}",
                    first_name=firstnames[i],
                    last_name=lastnames[i],
                    password="user_pass",
                )
                user.groups.add(customers_group)
                logging.warning(
                    f"User {i + 1} ({firstnames[i]} {lastnames[i]}) was created successfully!"
                )
            except IntegrityError:
                error_users += 1
                logging.error(
                    f"User {i + 1} ({firstnames[i]} {lastnames[i]}) was not created!"
                )

        if error_users:
            logging.error(f"{error_users} users were not created due to duplication.")

        # Create system admins
        admin_count = 5
        firstnames = [fake.unique.first_name() for _ in range(admin_count)]
        lastnames = [fake.unique.last_name() for _ in range(admin_count)]
        for i in range(admin_count):
            username = f"{firstnames[i][0]}.{lastnames[i].replace(' ', '')}".lower()
            user = User.objects.create_user(
                username=username,
                email=f"{username}@ocg.com",
                first_name=firstnames[i],
                last_name=lastnames[i],
                password="admin_pass",
            )
            user.groups.add(admins_group)
            logging.warning(
                f"Admin {i + 1} ({firstnames[i]} {lastnames[i]}) was created successfully!"
            )

        for user in User.objects.filter(groups=customers_group):
            full_name = f"{user.first_name} {user.last_name}"
            customer = Customer.objects.create(
                user=user,
                name=full_name,
                image=f"https://robohash.org/{full_name.lower().replace(' ', '')}",
            )
            logging.warning(f"Customer ({full_name}) was created successfully!")

        customers = Customer.objects.all()
        count_customers = Customer.objects.all().count()
        days_count = 90
        now = datetime.now()
        status_choices = [
            *("paid " * 10).strip().split(" "),
            *("pending " * 3).strip().split(" "),
        ]
        for days in range(days_count):
            today = now - timedelta(days=days)
            for _ in range(count_customers * 100 // days_count):
                invoice = Invoice.objects.create(
                    customer=random.choice(customers),
                    amount=random.random() * 2980 + 20,
                    date=today,
                    status=random.choice(status_choices),
                )
                logging.warning(f"Invoice ({invoice}) was created successfully!")
