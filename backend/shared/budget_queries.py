def get_budget(budget_id: str) -> dict | None:
    # Fetches a single budget by ID, returns None if not found


    return {}


def get_all_budgets() -> list:
    # Fetches all budget records


    return []


def get_budgets_by_period(period: str) -> list:
    # Fetches all budgets matching a specific period
    
    return []


def delete_budget(budget_id: str) -> bool:
    # Deletes a budget by ID, returns True if deleted, False if not found


    return True


def update_budget(budget_id: str, updates: dict) -> dict | None:
    # Updates specific fields on a budget, returns the updated record
    # Only keys present in updates are changed
    #
    # updates may contain any of:
    #   'name', 'amount', 'period', 'date', 'is_recurring'
    
    return {}