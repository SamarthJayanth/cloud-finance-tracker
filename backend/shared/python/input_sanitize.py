from errors import *
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
import json

# Create functions for period, name, etc
# Create allowable name types for entry


# This function is called when json encounters an object it cannot serialize
class DecimalEncoder(json.JSONEncoder):
    # Calls default, returns float type which is serializable
    def default(self, obj):
        if(isinstance(obj, Decimal)):
            return float(obj)
        # If the object is not Decimal type, then we allow json to raise the error
        return super().default(obj) 
    
def sanitize_amount(val):   
    try:
        amount = Decimal(str(val))    
    except (ValueError, TypeError, InvalidOperation):
        raise ValidInputError('Amount must be a number')
    if(amount < 0):
        raise ValidInputError('Amount must be positive')
    if(amount > 1000000):
        raise ValidInputError('Amount cannot exceed 1,000,000')
    return round(amount,2)
    
allowed_types = {'groceries', 'transport', 'utilities', 'shopping', 'housing', 'entertainment', 'luxuries', 'dining', 'any'}
allowed_goal_types = {'savings', 'investment', 'purchase', 'debt payoff', 'other'}
def sanitize_type(val, is_goal = False):
    if(val == None):
        raise ValidInputError('Type cannot be empty') 
    if(not (isinstance(val, str))):
        raise ValidInputError('Type must be a string') 
    val = val.strip().lower()
    if (len(val) > 100): # If user adds a custom type
        raise ValidInputError('Type cannot exceed 100 characters')
    if not is_goal:    
        if (not(val in allowed_types)):
            raise ValidInputError('Type cannot be different than allowed types')
    else:
        if(not (val in allowed_goal_types)):
            raise ValidInputError('Type cannot be different than allowed types')
    # Need to ensure no special characters
    # Can also have predetermined expense types(user can add them)
    return val

def sanitize_name(val):
    
    if(val == None):
        raise ValidInputError('Name cannot be empty') 
    if(not isinstance(val, str)):
            raise ValidInputError('Name must be a string') 
    val = val.strip().lower()
    if (len(val) > 100): # If user adds a custom type
        raise ValidInputError('Name cannot exceed 100 characters')
    # Need to ensure no special characters
    # Can also have predetermined expense names(user can add them)
    return val

def sanitize_date(val, allow_future: bool = False):
    # Date is of the form YYYY-MM-DD
    if(val == None):
        raise ValidInputError('Date is required') 
    val = str(val).strip() 
    if (len(val) > 10):
        raise ValidInputError('Date cannot exceed 10 characters, must be in YYYY-MM-DD format')
    try:
        # Convert into datetime obj to see if valid
        date_parsed = datetime.strptime(val, '%Y-%m-%d').date()
    except ValueError:
        raise ValidInputError('Date must be a valid date')
    if (date_parsed < date(2000, 1, 1)):
        raise ValidInputError('Date cannot be too far in the past')
    if (not allow_future) and (date_parsed > date.today()):
        raise ValidInputError('Date cannot be in the future')
    return str(date_parsed)
#Check dates in the future as well, import date lib

def sanitize_description(val):
    if(val == None):
        raise ValidInputError('Description cannot be empty') 
    if(not isinstance(val, str)):
        raise ValidInputError('Description must be a string') 
    val = val.strip().lower()
    if (len(val) > 500): 
        raise ValidInputError('Description cannot exceed 500 characters')
    return val

allowed_budget_periods = {'weekly', 'biweekly', 'monthly', 'quarterly', 'yearly'}
allowed_income_periods = {'one-time', 'weekly', 'biweekly', 'monthly', 'quarterly', 'yearly'}
# Since income can be one time, is has no delta time, so we use default parameter here to fix this issue
def sanitize_period(val, record_type = 'budget'):
    if(val == None):
        raise ValidInputError('Period cannot be empty')
    if(not isinstance(val, str)):
        raise ValidInputError('Period must be a string')
    val = val.strip().lower()
    if(len(val) > 50):
        raise ValidInputError('Period cannot be longer than 50 characters')
    if(record_type == 'income'):
        allowed_periods = allowed_income_periods
    elif(record_type == 'budget'):
        allowed_periods = allowed_budget_periods
    else:
        raise AppError('Invalid record type')
    if (not(val in allowed_periods)):
        raise ValidInputError('Period cannot be different than allowed types')
    return val
def sanitize_recurring(val):
    if(isinstance(val, bool)):
        return val
    if(isinstance(val, str)):
        if(val.strip().lower() == 'true'):
            return True
        if(val.strip().lower() == 'false'):
            return False
        
    raise ValidInputError('Recurrence must be set to true or false')
def sanitize_id(val):
    if(not val):
        raise ValueError('Id cannot be empty')
    else:
        return val