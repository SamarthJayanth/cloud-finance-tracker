from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from errors import *

all_period_config = {'weekly': {'delta_time': 1, 'which_time': 'weeks'},
                    'biweekly': {'delta_time': 2, 'which_time': 'weeks'}, 
                    'monthly': {'delta_time': 1, 'which_time': 'months'}, 
                    'quarterly': {'delta_time': 3, 'which_time': 'months'}, 
                    'yearly': {'delta_time': 1, 'which_time': 'years'}}

def get_period_delta(which_time, delta_time):

    match which_time:
        case 'weeks':
            return relativedelta(weeks = delta_time)
        case 'months':
            return relativedelta(months = delta_time)
        case 'years':
            return relativedelta(years = delta_time)
        case _:
            raise ValueError('Period must be an allowed period')

def get_current_period(budget: dict):
    budget_period = budget.get('period')
    budget_date = budget.get('start_date')
    is_recurring = budget.get('is_recurring')

    if budget_period not in all_period_config:
        raise ValueError(f'Invalid budget period: {budget_period}')

    period_config = all_period_config.get(budget_period)
    delta = get_period_delta(period_config['which_time'],period_config['delta_time'])

    start_date = datetime.strptime(budget_date, '%Y-%m-%d').date()

    if is_recurring:
        while start_date + delta <= date.today():
            start_date = start_date + delta
        end_date = start_date + delta - timedelta(days=1)
    else:
        if start_date + delta <= date.today():
            raise ExpiredError('Budget is expired')
        end_date = start_date + delta - timedelta(days=1)

    return start_date, end_date

def calculate_budget_status(amount_spent: float, amount_limit: float,
                            start_date, end_date) -> dict:
    
    # Calculates spending statistics for a budget.

    # Arguments:
    #     amount_spent (float): total spent in current period
    #     amount_limit (float): the budget limit
    #     start_date (date):    start of current period
    #     end_date (date):      end of current period

    # Returns:
    #     dict: {
    #         'amount_spent':     float,
    #         'amount_remaining': float,
    #         'amount_limit':     float,
    #         'percentage_used':  float,
    #         'days_elapsed':     int,
    #         'days_remaining':   int,
    #         'days_total':       int,
    #         'daily_average':    float,
    #         'projected_total':  float,
    #         'status':           str, 'on_track' / 'warning' / 'exceeded'
    #     }
    
    date_today = date.today()
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    days_total = (end_date - start_date).days + 1
    days_elapsed = (date_today - start_date).days + 1
    days_remaining = (end_date - date_today).days
    if days_remaining < 0:
        raise ExpiredError('Budget is expired')
    percentage_used = (amount_spent / amount_limit) * 100 if amount_limit > 0 else 0
    daily_average = amount_spent / days_elapsed if days_elapsed > 0 else 0
    projected_total = daily_average * days_total
    daily_recommended = amount_limit / days_total
    if amount_spent >= amount_limit:
        status = 'exceeded'
    elif percentage_used >= 80 or projected_total > amount_limit:
        status = 'warning'
    else:
        status = 'on_track'

    return {
        'amount_spent':     round(amount_spent, 2),
        'amount_remaining': round(amount_limit - amount_spent, 2),
        'amount_limit':     round(amount_limit, 2),
        'percentage_used':  round(percentage_used, 2),
        'days_elapsed':     days_elapsed,
        'days_remaining':   days_remaining,
        'days_total':       days_total,
        'daily_recommended':  round(daily_recommended, 2),
        'daily_average':    round(daily_average, 2),
        'projected_total':  round(projected_total, 2),
        'status':           status
    }