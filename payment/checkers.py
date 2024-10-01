from django.core.exceptions import ValidationError
from datetime import datetime

def card_number_checker (val):
    """
      Luhn ALgorthim for credit cared checker
    """
    # Remove any spaces or non-digit characters
    val = str(val)
    card_number = ''.join(filter(str.isdigit, val))
    
    # Check if the card number is valid
    if not card_number.isdigit() or len(card_number) < 2:
        return False
    
    # Reverse the card number for processing
    total = 0
    reverse_digits = card_number[::-1]
    
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        
        # Double every second digit
        if i % 2 == 1:
            n *= 2
            # If doubling results in a number > 9, subtract 9
            if n > 9:
                n -= 9
        
        total += n
    
    # The number is valid if the total modulo 10 is 0
    return total % 10 == 0



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
    