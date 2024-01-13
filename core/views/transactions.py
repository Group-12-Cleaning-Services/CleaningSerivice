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
import threading
import time


class PaymentViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def initialize_transaction(self, request):
        
        SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")
        service_id = request.data.get('service_id')
        user = get_user_from_jwttoken(request)
        # service_time = request.data.get('time')

        url="https://api.paystack.co/transaction/initialize"
        print(user)
        print(service_id)
        
        if user is None or service_id is None:
            context = {
                "error": "user and service id is required"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        email = user.email 
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
                verify_thread = threading.Thread(target=self.verify_transaction, args=[request, data["data"]["reference"]])
                verify_thread.start()
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(response.text, status=response.status_code)
        return Response({"error": "service not found"}, status=status.HTTP_404_NOT_FOUND)
            
    
    def verify_transaction(self, request ,reference)-> Response:
        
        time.sleep(120)
        SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")
        service_id = request.data.get('service_id')
        service_time = request.data.get('time')
        address = request.data.get('address')
        date = request.data.get('date')[0:10]
        user = get_user_from_jwttoken(request)

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
                schedule_service = book_service(service=service, user=user, time=service_time, address=address, date=date)
                print(schedule_service if schedule_service else "not booked")
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