import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *
from expense_queries import *

def lambda_handler(event: dict):
    fields = event.get('body')
    get_type = fields.get('type')
    match get_type: 
        case 'all':
            retrieve_all(fields)
        case'by_date_range':
            retrieve_by_date_range(fields)
        case 'type':
            retrieve_by_type(fields)
        case 'type_and_by_amount_range':
            retrieve_by_type_and_amount_range(fields)
        case 'amount_range':
            retrieve_by_amount_range(fields)