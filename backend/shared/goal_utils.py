from datetime import datetime, date
from errors import *
def calculate_goal_status(amount_spent, target_savings, income_earned, start_date, end_date):
    date_today = date.today()
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    days_total = (end_date - start_date).days + 1
    days_elapsed = (date_today - start_date).days + 1
    days_remaining = (end_date - date_today).days
    if (days_remaining) < 0:
        raise ExpiredError('Goal is expired')
    percentage_saved = (amount_spent / target_savings) * 100 if target_savings > 0 else 0
    daily_average_savings = (income_earned-amount_spent) / days_elapsed if days_elapsed > 0 else 0
    projected_savings = daily_average_savings * days_total
    daily_recommended_savings = target_savings / days_total
    if daily_average_savings < daily_recommended_savings:
        status = 'warning'
    else:
        status = 'on_track'

    return {
        'amount_spent': round(amount_spent, 2),
        'target_savings': target_savings,
        'percentage_saved': round(percentage_saved, 2),
        'days_elapsed': days_elapsed,
        'days_remaining': days_remaining,
        'days_total': days_total,
        'daily_recommended_savings': round(daily_recommended_savings, 2),
        'daily_average_savings': round(daily_average_savings, 2),
        'projected_savings': round(projected_savings, 2),
        'status': status
    }
