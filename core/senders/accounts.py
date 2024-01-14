from core.models import CleaningServiceUser, VerificationToken, PasswordToken
from django.contrib.auth import get_user_model
import random, string
from core.serializers import CleaningServiceSerializer
import requests
import pytz
from datetime import datetime, timedelta

UTC = pytz.UTC

def create_user(email, password):
    """Create user"""
    user = CleaningServiceUser.objects.create_user(email=email, password=password)
    return user

# def create_user(data):
#     serializer = CleaningServiceSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return serializer.data
#     else:
#         return serializer.error

def get_all_service_providers()-> CleaningServiceUser:
    """Get all service providers"""
    query_set = CleaningServiceUser.objects.filter(user_type='service_provider')
    serializer = CleaningServiceSerializer(query_set, many=True)
    return serializer.data

    
    
def generate_token(otp_length):
    """Generate token"""
    return ''.join([random.choice(string.ascii_uppercase + string.digits)] for _ in range(otp_length))


def create_verification_token(email, token):
    """Create verification token"""
    time_generated = UTC.localize(datetime.now())
    print(f"time: {time_generated}")
    verification_token = VerificationToken.objects.create(email=email, token=token, time=time_generated)
    return verification_token


def update_verification_token(verification_token, token):
    """Update verification token"""
    time_generated = UTC.localize(datetime.now())
    verification_token.token = token
    verification_token.time = time_generated
    verification_token.save()
    return verification_token


def create_password_token(email, token):
    """Create password token"""
    time_generated = UTC.localize(datetime.now())
    password_token = PasswordToken.objects.create(email=email, token=token, time=time_generated)
    return password_token


def update_password_token(password_token, token):
    """Update password token"""
    time_generated = UTC.localize(datetime.now())
    password_token.token = token
    password_token.time = time_generated
    password_token.save()
    return password_token

def create_transfer_receipient(profile):
    """Create transfer receipient"""
    name = f"{profile.first_name} {profile.last_name}"
    account_number = profile.contact
    bank_code = None
    url = "https://api.paystack.co/transferrecipient"
    currency = "GHS"
    if (profile.contact.startswith("024") or profile.contact.startswith("054") or profile.contact.startswith("055") or profile.contact.startswith("059")):
        bank_code = "MTN"
    elif (profile.contact.startswith("020") or profile.contact.startswith("050") or profile.contact.startswith("056")):
        bank_code = "VOD"
    elif (profile.contact.startswith("026") or profile.contact.startswith("056") or profile.contact.startswith("057") or profile.contact.startswith("027") or profile.contact.startswith("057") or profile.contact.startswith("057")):
        bank_code = "ATL"
    
    PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")

    headers = {
        Authorization: f"Bearer {PAYSTACK_SECRET_KEY}",
        Content-Type: application/json
    }
    data = {
        "type": "mobile_money",
        "name": name,
        "account_number": account_number,
        "bank_code": bank_code,
        "currency": currency
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    return response.json()