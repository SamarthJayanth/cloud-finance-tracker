import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from input_sanitize import *

def lambda_handler(event: dict):
    fields = event.get('body')
    id = fields.get('id')
    
    # Retrieve budget for the certain type
    pass