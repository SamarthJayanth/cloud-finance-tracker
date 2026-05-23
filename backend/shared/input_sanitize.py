from errors import *
from datetime import datetime, date

# Create functions for period, name, etc
# Create allowable name types for entry


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
    
allowed_types = {'groceries', 'transport', 'utilities', 'shopping', 'housing', 'entertainment', 'luxuries', 'dining', 'any'}
# Hardcoded types but will change when integrated with lambda
def sanitize_type(val):
    if(val == None or type(val)!='str'):
            raise ValidInputError('Type must be a string') 
    val = val.strip().lower()
    # Must recheck
    if (val == None):
        raise ValidInputError('Type cannot be empty') 
    if (len(val) > 100): # If user adds a custom type
        raise ValidInputError('Type cannot exceed 100 characters')
    if (not(val in allowed_types)):
        raise ValidInputError('Type cannot be different than allowed types')
    # Need to ensure no special characters
    # Can also have predetermined expense types(user can add them)
    return val
    
def sanitize_date(val):
    # Date is of the form YYYY-MM-DD
    if(val == None):
        raise ValidInputError('Date is required') 
    val = str(val).strip() 
    # Must recheck
    if (val == None):
        raise ValidInputError('Date cannot be empty') 
    if (len(val) > 10):
        raise ValidInputError('Date cannot exceed 10 characters, must be in YYYY-MM-DD format')
    try:
        # Convert into datetime obj to see if valid
        date_parsed = datetime.strptime(val, '%Y-%m-%d').date()
    except :
        raise ValidInputError('Date must be a valid date')
    if (date_parsed > date.today()):
        raise ValidInputError('Date cannot be in the future')
    if (date_parsed < date(2000, 1, 1)):
        raise ValidInputError('Date cannot be too far in the past')
    return str(date_parsed)
#Check dates in the future as well, import date lib

def sanitize_description(val):
    if(val == None):
        raise ValidInputError('Description cannot be empty') 
    if(type(val)!='str'):
        raise ValidInputError('Description must be a string') 
    val = val.strip().lower()
    # Must recheck
    if (val == None):
        raise ValidInputError('Description cannot be empty') 
    if (len(val) > 500): 
        raise ValidInputError('Description cannot exceed 500 characters')
    return val

allowed_periods = {'weekly', 'biweekly', 'monthly', 'quarterly', 'yearly'}
def sanitize_period(val):
    if(val == None):
        raise ValidInputError('Period cannot be empty')
    if(type(val)!='str'):
        raise ValidInputError('Period must be a string')
    val = val.strip().lower()
    if(val == None):
        raise ValidInputError('Period cannot be empty')
    if(len(val) > 50):
        raise ValidInputError('Period cannot be longer than 50 characters')
    if (not(val in allowed_periods)):
        raise ValidInputError('Period cannot be different than allowed types')
    return val