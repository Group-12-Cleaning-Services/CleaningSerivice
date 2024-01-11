from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.senders.accounts import *
from core.senders.services import *
from core.retrievers.accounts import *
from core.retrievers.services import *
from core.models import Transaction
import requests
from core.utils import *
import json
import os


class PaymentViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def initialize_transaction(self, request):
        
        SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")
        service_id = request.data.get('service_id')
        user = get_user_from_jwttoken(request)
        time = request.data.get('time')

        url="https://api.paystack.co/transaction/initialize"
        
        if user is None or service_id is None:
            context = {
                "error": "user and service id is required"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        email = user.email 
        print()
        service = get_service_by_id(service_id)
        if service:
            data = {
                "email": email,
                "amount": str(service.price * 100),
                "currency": 'GHS'
            }
            headers = {
            "Authorization": f"Bearer {SECRET_KEY}",
            "Content-Type": "application/json"
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                data = response.json()
                return Response(data, status=response.status_code)
            else:
                return Response(response.text, status=response.status_code)
        return Response({"error": "service not found"}, status=status.HTTP_404_NOT_FOUND)
            
    
    def verify_transaction(self, request)-> Response:
        
        
        SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")
        user = get_user_from_jwttoken(request)
        service_id = request.data.get('service_id')
        time = request.data.get('time')
        reference = request.data.get('reference')


        if not user or not service_id:
            context = {
                "error": "user and service id is required"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        if not user:
            context = {
                "error": "user is required"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        if not reference:
            context = {
                "error": "reference is required"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        
        headers = {
            "Authorization": f"Bearer {SECRET_KEY}",
            "Content-Type": "application/json"
            }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            response = response.json()
            if response["data"]["status"] == "success":
                service = get_service_by_id(service_id)
                schedule_service = book_service(service=service, user=user, time=time)
                Transaction.objects.create(user=user, balance=service.price)
                context = {
                    "detail": "Service booked successfully",
                    "data": schedule_service
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {
                    "detail": "Transaction failed"
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response.text, status=response.status_code)