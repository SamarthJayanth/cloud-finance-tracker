import boto3
import json
from decimal import Decimal # DynamoDB doesn't take float values
from datetime import date
from input_sanitize import *
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')
table = dynamodb.Table('goals')

earliest_date = '2000-01-01'
def get_goal_by_id(user_id: str, goal_id: str) -> dict | None:
    # Fetches a single goal by id, returns None if not found
    try:
        response = table.get_item(Key = {
            'user_id': user_id,
            'goal_id': goal_id
        })
        return response.get('Item')
        # return from goals_table
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to get goal')
    
def get_goals(user_id: str, name: str = None, start_date: str = earliest_date, end_date: str = None,
                 min_amount: float = None, max_amount: float = None):
    # Returns list of expense records matching filters
    if end_date is None:
        end_date = str(date.today())
    try:
        filter_expr = Attr('start_date').between(start_date, end_date)
        if name:
            filter_expr = filter_expr & Attr('name').eq(name)
        if min_amount is not None: # Evaluate here because min amt could be 0
            filter_expr = filter_expr & Attr('amount').gt(min_amount)
        if max_amount is not None: 
            filter_expr = filter_expr & Attr('amount').lt(max_amount)
        response = table.query(
            KeyConditionExpression = Key('user_id').eq(user_id),
            FilterExpression = filter_expr
            )
        return response.get('Items', [])
    except Exception as e:
        print(f'Dynamodb error: {str(e)}')
        raise DataBaseError('Failed to get goals')

def add_goal(goal: dict):
    try:
        table.put_item(Item = goal)
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to add goal')

    
def delete_goal(user_id: str, goal_id: str):
    # Deletes a goal by id
    try:
        table.delete_item(Key = {'user_id': user_id, 'goal_id': goal_id})
    except Exception as e:
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to delete goal')

def edit_goal(goal: dict) -> dict | None:
    # Updates specific fields on a goal
    # Only keys present in updates are changed
    goal_id = goal.pop('goal_id')
    user_id = goal.pop('user_id')
    try:
        update_parts = []
        expr_attr_names = {}
        expr_attr_vals = {}
        for i, k in enumerate(goal.keys()):
            update_parts.append(f'#k{i} = :v{i}')
            expr_attr_names[f'#k{i}'] = k
            expr_attr_vals[f':v{i}'] = goal.get(k)
        update_expr = 'SET '+' , '.join(update_parts)
        table.update_item(
            Key = {
                'user_id': user_id,
                'goal_id': goal_id
            },
        ConditionExpression = Attr('goal_id').exists(),
        UpdateExpression = update_expr,
        ExpressionAttributeNames = expr_attr_names,
        ExpressionAttributeValues = expr_attr_vals
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise NotFoundError('Goal not found')
        print(f'DynamoDB error: {str(e)}')
        raise DataBaseError('Failed to update goal')
    except Exception as e:
        print(f'DynamoDB error {str(e)}')
        raise DataBaseError('Failed to update goal')