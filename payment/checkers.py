from django.core.exceptions import ValidationError
from datetime import datetime

def card_number_checker (val):
    return True

def card_cvc_checker (val):
    val = str(val)

    if len(val) != 3 :
        return False

    return True

def card_exp_checker (val):
    val = str(val)

    if len(val) != 5 or val[2] != '/' :
        return False 

    month, year = val.split('/')

    if int(month) > 12 :
        return False
    
    card_year = int(f"20{year}")
    now_year = datetime.now().year

    if card_year < now_year : 
        return False
    
    return True
    