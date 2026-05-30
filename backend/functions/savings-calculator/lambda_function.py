import json
import uuid
import boto3
from datetime import date
from decimal import Decimal # DynamoDB doesn't take float values
from input_sanitize import * # comes from layer automatically
from errors import * # comes from layer automatically

dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
expense_table = dynamodb.Table('expense')
income_table = dynamodb.Table('income')
def lambda_handler(event: dict, context):
    # Returns how much has been saved in a certain period of time
    # Date is optional
    fields = event.get('body') if event.get('body') else {}
    start_date = fields.get('start_date')
    end_date = fields.get('end_date')
    if (start_date and end_date):
        start_date = sanitize_date(start_date)
        end_date = sanitize_date(end_date)
        if (end_date < start_date): # We can do this because of the ordering format
            raise ValidInputError('End date cannot be before start date')
        income_items = get_income_in_range(start_date, end_date)
        expense_items = get_expenses_in_range(start_date, end_date)
    elif (start_date or end_date):
        raise ValidInputError('Both start and end date required')
    else:
        income_items = get_all_income()