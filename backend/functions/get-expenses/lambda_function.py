import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
from expense_queries import *
def lambda_handler(event: dict):
    fields = event.get('body')
    get_type = fields.get('type')
    match get_type: 
        case'above_amount':
            retrieve_above_amount(fields)
        case'below_amount':
            retrieve_below_amount(fields)
        case'after_date':
            retrieve_after_date(fields)
        case'before_date':
            retrieve_before_date(fields)
        case'in_date_range':
            retrieve_in_date_range(fields)
        case 'type':
            retrieve_by_type(fields)
        case 'type_and_in__range':
            retrieve_by_type_and_range(fields)