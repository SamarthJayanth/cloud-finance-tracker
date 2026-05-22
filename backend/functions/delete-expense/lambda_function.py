import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

def lambda_handler(event: dict):
    fields = event.get('body')
    id = fields.get('id')
    date = sanitize_date(fields.get('date')) # For good measure
    # Need id and date to reconstruct the actual expense id
    # For proper security, we must ensure that the request is sent by an authorized user

    # Remove from data base