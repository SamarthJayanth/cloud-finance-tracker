from errors import *

def sanitize_amount(val):   
    try:
        amount = float(val)    
    except (ValueError or TypeError):
        raise ValidInputError('Amount must be a number')
    if(amount < 0):
        raise ValidInputError('Amount must be positive')
    if(amount > 1000000):
        raise ValidInputError('Amount cannot exceed 1,000,000')
    return round(amount,2)
    
def sanitize_type(val):
    if(val == None or type(val)!='str'):
            raise ValidInputError('Type must be a string') 
    val = val.strip().lower()
    # Must recheck
    if (val == None):
        raise ValidInputError('Type cannot be empty') 
    if (len(val) > 100):
        raise ValidInputError('Type cannot exceed 100 characters')
    # Need to ensure no special characters
    # Can also have predetermined expense types(user can add them)
    return val
    
def sanitize_date(val):
    if(val == None):
        raise ValidInputError('Date is required') 
    val = val.strip().lower()
    # Must recheck
    if (val == None):
        raise ValidInputError('Date cannot be empty') 
    if (len(val) > 100):
        raise ValidInputError('Date cannot exceed 100 characters')
    return val
#Check dates in the future as well, import date lib
    

def sanitize_description(val):
    if(val == None or type(val)!='str'):
            raise ValidInputError('Description must be a string') 
    val = val.strip().lower()
    # Must recheck
    if (val == None):
        raise ValidInputError('Description cannot be empty') 
    if (len(val) > 500):
        raise ValidInputError('Description cannot exceed 500 characters')
    return val
    
