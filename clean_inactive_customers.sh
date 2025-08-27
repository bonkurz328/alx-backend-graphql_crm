#!/bin/bash

# Get the absolute path to the Django project directory (adjust based on your setup)
DJANGO_DIR="/home/ubuntu/alx-backend-graphql_crm/crm"

# Change to the Django project directory
cd "$DJANGO_DIR" || exit 1

# Execute Python command to delete inactive customers and log the results
python manage.py shell << EOF
from django.utils import timezone
from datetime import timedelta
from customers.models import Customer, Order  # Using your customers app
import datetime

# Calculate date one year ago
one_year_ago = timezone.now() - timedelta(days=365)

# Find customers with no orders since one year ago
# Adjust this query based on your actual model relationships
inactive_customers = Customer.objects.filter(
    orders__isnull=True  # Assuming related_name='orders'
) | Customer.objects.filter(
    orders__created_at__lt=one_year_ago
).distinct()

# Count before deletion
count_before = inactive_customers.count()

# Delete inactive customers
inactive_customers.delete()

# Log results
log_message = f"[{datetime.datetime.now()}] Deleted {count_before} inactive customers\n"
with open('/tmp/customer_cleanup_log.txt', 'a') as log_file:
    log_file.write(log_message)

print(f"Successfully deleted {count_before} inactive customers")
EOF
