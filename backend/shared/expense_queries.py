import boto3
import json
from decimal import Decimal # DynamoDB doesn't take float values
from datetime import date
from input_sanitize import *
from boto3.dynamodb.conditions import Key, Attr
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
    try:
        filter_expr = Attr('date').between(start_date, end_date)
        if expense_type:
            filter_expr = filter_expr & Attr('type').eq(expense_type)
        if min_amount is not None: # Evaluate here because min amt could be 0
            filter_expr = filter_expr & Attr('amount').gt(min_amount)
        if max_amount is not None: 
            filter_expr = filter_expr & Attr('amount').lt(max_amount)
        response = table.scan(FilterExpression = filter_expr)
        return response.get('Items', [])
    except Exception as e:
        print(f'Dynamodb error: {str(e)}')
        raise DataBaseError('Failed to get expenses')
    

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

def edit_expense(expense: dict):
    expense_id = expense.pop('id') # So id is not updated
    try: 
        update_parts = []
        expr_attr_names = {}
        expr_attr_vals = {}
        for i, k in enumerate(expense.keys()):
            update_parts.append(f'#k{i} = :v{i}')
            expr_attr_names[f'#k{i}'] = k
            expr_attr_vals[f':v{i}'] = expense[k]
            # Need # because it is a required syntax
            # Dynamodb has some reserved names, so we use k+KEY as a label
        update_expr = 'SET ' + ', '.join(update_parts)      # join all pairs at end
        table.update_item(
    Key={
        'id': expense_id,
    },
    UpdateExpression = update_expr,
    ExpressionAttributeNames = expr_attr_names,
    ExpressionAttributeValues = expr_attr_vals
    )
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        raise DataBaseError('Failed to update expense')
    

def delete_expense(expense_id: str):
    try:
        table.delete_item(Key = {'id': expense_id})
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to delete expense')
    

def expense_by_id(expense_id: str):
    try:
        response = table.query(KeyConditionExpression = Key('id').eq(expense_id))
        return response.get('Items')[0] if response.get('Items') else None
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to retrieve expense')