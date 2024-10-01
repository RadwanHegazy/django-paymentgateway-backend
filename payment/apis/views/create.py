from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from ..serializers import ClientPaymentSerializer, Payment
from datetime import datetime

class CreatePayment (APIView) : 
    serializer_class = ClientPaymentSerializer

    def post(self, request, id) : 
        try : 
            payment = Payment.objects.get(id=id, is_done=False)
        except Payment.DoesNotExist:
            return Response({
                'message' : "payment not found"
            }, status=status.HTTP_404_NOT_FOUND)

        if datetime.now().timestamp() > payment.exp_at.timestamp():
            payment.delete()
            return Response({
                'message' : "payment not found"
            }, status=status.HTTP_404_NOT_FOUND)
                
        sr = self.serializer_class(payment, data=request.data)
        if sr.is_valid() : 
            sr.save()
            payment.is_done = True
            payment.save()
            payment.user.balance += payment.amount
            payment.user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(sr.errors, status=status.HTTP_400_BAD_REQUEST)


class OwnerCreatePayment (APIView) : 
    permission_classes = [permissions.IsAuthenticated]

    def post (self, request) : 
        amount = request.data.get('amount', None)
        if amount is None :
            return Response({'message':"amount not found"}, status=status.HTTP_400_BAD_REQUEST)
        amount = float(amount)
        user = request.user
        py = Payment.objects.create(
            user=user,
            amount=amount
        )
        py.save()

        return Response({
            'id' : str(py.id)
        }, status=status.HTTP_201_CREATED)