from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from ..serializers import OwnerPaymentSerializer, Payment

class GetClientPayment (APIView) :
    
    def get(self, request, id) : 
        try : 
            payment = Payment.objects.get(id=id, is_done=False)
        except Payment.DoesNotExist:
            return Response({
                'message' : 'payment not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'amount' : payment.amount
        }, status=status.HTTP_200_OK)
    

class GetOwnerPayments (APIView) : 
    serializer_class = OwnerPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) :
        user = request.user
        payments = Payment.objects.filter(user=user, is_done=True)
        sr = self.serializer_class(payments, many=True)
        return Response(sr.data, status=status.HTTP_200_OK)