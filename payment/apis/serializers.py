from rest_framework import serializers
from .. import checkers
from ..models import Payment
from rest_framework.validators import ValidationError

class ClientPaymentSerializer (serializers.ModelSerializer) : 
    
    class Meta:
        model = Payment
        fields = ["card_number","card_cvc","card_exp",
                  "full_name","email"]
        
    def validate (self, attrs) : 
        card_number = attrs.get('card_number')
        card_cvc = attrs.get('card_cvc')
        card_exp = attrs.get('card_exp')

        if not checkers.card_cvc_checker(card_cvc) : 
            raise ValidationError({
                'message' : 'invalid card_cvc value'
            })
        
        if not checkers.card_exp_checker(card_exp):
            raise ValidationError({
                'message' : 'invalid card_exp value'
            })


        if not checkers.card_number_checker(card_number):
            raise ValidationError({
                'message' : 'invalid card_exp value'
            })
        
        return attrs
    
class OwnerPaymentSerializer (serializers.ModelSerializer) :
    class Meta:
        model = Payment
        fields = ["id","amount","state","datetime",'full_name',"email"]
