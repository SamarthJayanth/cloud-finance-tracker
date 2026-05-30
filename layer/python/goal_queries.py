def get_goal(goal_id: str) -> dict | None:
    # Fetches a single goal by id, returns None if not found
    
    # return from goals_table
    return {}


def get_all_goals() -> list:
    # Fetches all goal records

    # Return from goals_table
    return []


def delete_goal(goal_id: str) -> bool:
    # Deletes a goal by ID, returns True if deleted, False if not found


    # return True if success, else False
    return True

def update_goal(goal_id: str, updates: dict) -> dict | None:
    # Updates specific fields on a goal, returns the updated record
    # Only keys present in updates are changed

    return {}