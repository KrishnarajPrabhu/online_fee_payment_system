import os
import django
from django.contrib.auth.hashers import make_password

# Configure settings for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payment_system.settings')
django.setup()

# Hash the password
password = "miniproject"  # Replace with your actual plain text password
hashed_password = make_password(password)
print("Hashed Password:", hashed_password)
