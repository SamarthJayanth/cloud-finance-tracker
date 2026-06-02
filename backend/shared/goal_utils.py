from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def calculate_goal_status():
        pass


        
# start_date = goal.get('start_date')
# total_income = get_total_income(sanitize_date(start_date),str(date.today()))
#         all_expenses = get_expenses_by_date_range(sanitize_date(start_date),str(date.today()))
#         total_expenses = sum(exp.get('amount', 0) for exp in all_expenses)
#         percentage_to_goal = (total_income / total_expenses)
#         if (percentage_to_goal > 1.00):
#             # Goal reached
#     return
# projected_delta_days = ((date.today()-datetime.strptime(start_date, '%Y-%m-%d')).days)/percentage_to_goal
# projected_delta_days = math.ceil(projected_delta_days)
# projected_end_date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days = projected_delta_days)