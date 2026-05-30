import boto3
import json
from decimal import Decimal # DynamoDB doesn't take float values
from datetime import date
from input_sanitize import *
dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
table = dynamodb.Table('expenses')


# Need to extract expenses from specific dates
# Extract expenses from ranges, for the month, day, above a specific amount, etc

# Event will pass the type of call
# This can be either a range of dates, after/before, above/below an amount
earliest_date = '2000-01-01'
def get_expenses(start_date: str = earliest_date, end_date: str = None,
                 expense_type: str = None, min_amount: float = None, max_amount: float = None):
    # Returns list of expense records matching filters
    if end_date is None:
        end_date = str(date.today())
    pass

def get_total_expenses(start_date: str = earliest_date, end_date: str = None,
                       expense_type: str = None, min_amount: float = None, max_amount: float = None):
    # Returns single sum — just calls get_expenses and sums
    items = get_expenses(start_date, end_date, expense_type, min_amount, max_amount)
    return sum(item.get('amount') for item in items)
def add_expense(expense: dict):
    try:
        table.put_item(Item = expense)
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to save expense')
    return {
        'statusCode': 201,
        'body': json.dumps({
            'message': 'Expense added successfully',
            'expense': expense
        })
    }

def edit_expense():
    pass
def delete_expense():
    pass