import boto3
import json
from decimal import Decimal # DynamoDB doesn't take float values
from datetime import date
from input_sanitize import *
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
table = dynamodb.Table('incomes')

earliest_date = '2000-01-01'
def get_incomes(start_date: str = earliest_date, end_date: str = None,
                 min_amount: float = None, max_amount: float = None, period: str = None):
    # Returns list of income records matching filters
    if end_date is None:
        end_date = str(date.today())
    try:
        filter_expr = Attr('date').between(start_date, end_date)
        if min_amount is not None: # Evaluate here because min amt could be 0
            filter_expr = filter_expr & Attr('amount').gt(min_amount)
        if max_amount is not None: 
            filter_expr = filter_expr & Attr('amount').lt(max_amount)
        if period is not None:
            filter_expr = filter_expr & Attr('period').eq(period)
        response = table.scan(FilterExpression = filter_expr)
        return response.get('Items', [])
    except Exception as e:
        print(f'Dynamodb error: {str(e)}')
        raise DataBaseError('Failed to get incomes')
def get_total_income(start_date: str = earliest_date, end_date: str = None,
                 min_amount: float = None, max_amount: float = None, period: str = None):
    incomes = get_incomes(start_date, end_date, min_amount, max_amount, period)
    return sum(income.get('amount') for income in incomes)
    
income_config = {'one-time' : 1, 'weekly' : 52, 'biweekly' : 26, 'monthly' : 12, 'quarterly' : 4, 'yearly' : 1}
def get_total_yearly_income(start_date: str = earliest_date, end_date: str = None,
                        min_amount: float = None, max_amount: float = None, period: str = None):
    # Returns single sum — just calls get_incomes and sums
    items = get_incomes(start_date, end_date, min_amount, max_amount, period)
    sum_items = 0
    for item in items:
        sum_items = sum_items + item.get('amount')*(income_config.get(item.get('period')))
    return sum_items

def get_total_yearly_recurring_income(start_date: str = earliest_date, end_date: str = None,
                        min_amount: float = None, max_amount: float = None, period: str = None):
    # Returns single sum — just calls get_incomes and sums
    items = get_incomes(start_date, end_date, min_amount, max_amount, period)
    sum_items = 0
    for item in items:
        if(item.get('period') == 'one-time'):
            continue
        sum_items = sum_items + item.get('amount')*(income_config.get(item.get('period')))
    return sum_items

def get_recurring_income():
    try:    
        response = table.scan(
            FilterExpression = Attr('period').ne('one-time')
        )
        return response.get('Items', [])
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to get recurring incomes')
def add_income(income: dict):
    try:
        table.put_item(Item = income)
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to add income')
    
def edit_income(income: dict) -> dict | None:
    # Updates specific fields on a income
    # Only keys present in updates are changed
    income_id = income.pop('id')
    try:
        update_parts = []
        expr_attr_names = {}
        expr_attr_vals = {}
        for i, k in enumerate(income.keys()):
            update_parts.append(f'#k{i} = :v{i}')
            expr_attr_names[f'#k{i}'] = k
            expr_attr_vals[f':v{i}'] = income.get(k)
        update_expr = 'SET '+' , '.join(update_parts)
        table.update_item(
            Key = {
                'id': income_id
            },
            ConditionExpression = Attr('id').exists(),
            UpdateExpression = update_expr,
            ExpressionAttributeNames = expr_attr_names,
            ExpressionAttributeValues = expr_attr_vals
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise NotFoundError('Income not found')
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to update income')
    except Exception as e:
        print(f'DynamoDB error {str(e)}')
        raise DataBaseError('Failed to update income')
    
def delete_income(income_id: str):
    # Deletes an income by id
    try:
        table.delete_item(Key = {'id': income_id})
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to delete income')

def get_income_by_id(income_id: str) -> dict | None:
    # Fetches a single income by id, returns None if not found
    try:
        response = table.query(KeyConditionExpression = Key('id').eq(income_id))
        income = response.get('Items')[0] if response.get('Items') else None
        # return from income_table
        return income
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to get income')
