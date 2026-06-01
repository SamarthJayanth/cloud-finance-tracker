import boto3
import json
from decimal import Decimal # DynamoDB doesn't take float values
from datetime import date
from input_sanitize import *
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
table = dynamodb.Table('budgets')

earliest_date = '2000-01-01'

def get_budgets(start_date: str = earliest_date, end_date: str = None, budget_type: str = None,
                 min_amount: float = None, max_amount: float = None, period: str = None):
    # Returns list of budget records matching filters
    if end_date is None:
        end_date = str(date.today())
    try:
        filter_expr = Attr('date').between(start_date, end_date)
        if budget_type is not None:
            filter_expr = filter_expr & Attr('type').eq(budget_type)
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
        raise DataBaseError('Failed to get budgets')
budget_config = {'weekly' : 52, 'biweekly' : 26, 'monthly' : 12, 'quarterly' : 4, 'yearly' : 1}
def get_total_yearly_budget(start_date: str = earliest_date, end_date: str = None, budget_type: str = None,
                 min_amount: float = None, max_amount: float = None, period: str = None):
    # Returns single sum — just calls get_budgets and sums
    items = get_budgets(start_date, end_date, budget_type, min_amount, max_amount, period)
    sum_items = 0
    for item in items:
        sum_items = sum_items + item.get('amount')*(budget_config.get(item.get('period')))
    return sum_items
def add_budget(budget: dict):
    try:
        table.put_item(Item = budget)
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to add budget')
def edit_budget(budget: dict) -> dict | None:
    # Updates specific fields on a budget
    # Only keys present in updates are changed
    budget_id = budget.pop('id')
    try:
        update_parts = []
        expr_attr_names = {}
        expr_attr_vals = {}
        for i, k in enumerate(budget.keys()):
            update_parts.append(f'#k{i} = :v{i}')
            expr_attr_names[f'#k{i}'] = k
            expr_attr_vals[f':v{i}'] = budget.get(k)
        update_expr = 'SET '+' , '.join(update_parts)
        table.update_item(
            Key = {
                'id': budget_id
            },
            UpdateExpression = update_expr,
            ExpressionAttributeNames = expr_attr_names,
            ExpressionAttributeValues = expr_attr_vals
        )
    except Exception as e:
        print(f'DynamoDB error {str(e)}')
        raise DataBaseError('Failed to edit budget')
def delete_budget(budget_id: str):
    # Deletes an budget by id
    try:
        table.delete_item(Key = {'id': budget_id})
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to delete budget')

def get_budget_by_id(budget_id: str) -> dict | None:
    # Fetches a single budget by id, returns None if not found
    try:
        response = table.query(KeyConditionExpression = Key('id').eq(budget_id))
        budget = response.get('Items')[0] if response.get('Items') else None
        # return from budget_table
        return budget
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to get budget')
