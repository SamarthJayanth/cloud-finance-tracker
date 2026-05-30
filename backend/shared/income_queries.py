from datetime import datetime, date

earliest_date = '2000-01-01'
def get_income(start_date: str = earliest_date, end_date: str = None,
                 expense_type: str = None, min_amount: float = None, max_amount: float = None):
    # Returns list of expense records matching filters
    if end_date is None:
        end_date = str(date.today())
    pass

def get_total_income(start_date: str = earliest_date, end_date: str = None,
                       expense_type: str = None, min_amount: float = None, max_amount: float = None):
    # Returns single sum — just calls get_expenses and sums
    items = get_income(start_date, end_date, expense_type, min_amount, max_amount)
    return sum(item.get('amount') for item in items)
def add_income():
    pass
def edit_income():
    pass
def delete_income():
    pass