from errors import *

def sanitize_amount(val):
    try:
        amount = float(val) 
        if(amount <= 0):
            raise ValidInputError('Amount must be positive') #Doesn't work yet
        if(amount > 1000000):
            raise ValidInputError('Amount cannot exceed 1,000,000')
        return round(amount,2)
        
    except (ValidInputError):
        raise ValidInputError('Amount must be a valid number')
    except (ValueError):
        raise ValidInputError('Amount must be a number')
    
def sanitize_type(val):
    return val
    pass
def sanitize_date(val):
    return val
    pass

def sanitize_description(val):
    return val
    pass