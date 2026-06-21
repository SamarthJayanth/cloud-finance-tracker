# This is what we attach to all roles, such that 
# any future policies we attach to a lambda role
# They will be assumed
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy" "lambda_basic_execution" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


resource "aws_iam_role" "add_budget" {
  name               = "add_budget_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "add_budget_put_item" {
  role       = aws_iam_role.add_budget.name
  policy_arn = aws_iam_policy.DynamoDB_PutItem.arn
}
resource "aws_iam_role_policy_attachment" "add_budget_basic_execution" {
  role       = aws_iam_role.add_budget.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "add_expense" {
  name               = "add_expense_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "add_expense_put_item" {
  role       = aws_iam_role.add_expense.name
  policy_arn = aws_iam_policy.DynamoDB_PutItem.arn
}
resource "aws_iam_role_policy_attachment" "add_expense_basic_execution" {
  role       = aws_iam_role.add_expense.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "add_goal" {
  name               = "add_goal_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "add_goal_put_item" {
  role       = aws_iam_role.add_goal.name
  policy_arn = aws_iam_policy.DynamoDB_PutItem.arn
}
resource "aws_iam_role_policy_attachment" "add_goal_basic_execution" {
  role       = aws_iam_role.add_goal.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "add_income" {
  name               = "add_income_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "add_income_put_item" {
  role       = aws_iam_role.add_income.name
  policy_arn = aws_iam_policy.DynamoDB_PutItem.arn
}
resource "aws_iam_role_policy_attachment" "add_income_basic_execution" {
  role       = aws_iam_role.add_income.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "budget_alert" {
  name               = "budget_alert_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "budget_alert_scan_item" {
  role       = aws_iam_role.budget_alert.name
  policy_arn = aws_iam_policy.DynamoDB_ScanItem.arn
}
resource "aws_iam_role_policy_attachment" "budget_alert_basic_execution" {
  role       = aws_iam_role.budget_alert.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}
resource "aws_iam_role_policy" "budget_alert_sns_publish" {
  name = "budget_alert_sns_publish_tf"
  role = aws_iam_role.budget_alert.id

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "sns:Publish",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:sns:${var.aws_region}:${var.aws_account_id}:budget-alerts"
      },
    ]
  })
}

resource "aws_iam_role" "daily_average" {
  name               = "daily_average_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "daily_average_query_item" {
  role       = aws_iam_role.daily_average.name
  policy_arn = aws_iam_policy.DynamoDB_QueryItem.arn
}
resource "aws_iam_role_policy_attachment" "daily_average_basic_execution" {
  role       = aws_iam_role.daily_average.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "delete_budget" {
  name               = "delete_budget_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "delete_budget_delete_item" {
  role       = aws_iam_role.delete_budget.name
  policy_arn = aws_iam_policy.DynamoDB_DeleteItem.arn
}
resource "aws_iam_role_policy_attachment" "delete_budget_basic_execution" {
  role       = aws_iam_role.delete_budget.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "delete_expense" {
  name               = "delete_expense_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "delete_expense_delete_item" {
  role       = aws_iam_role.delete_expense.name
  policy_arn = aws_iam_policy.DynamoDB_DeleteItem.arn
}
resource "aws_iam_role_policy_attachment" "delete_expense_basic_execution" {
  role       = aws_iam_role.delete_expense.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "delete_goal" {
  name               = "delete_goal_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "delete_goal_delete_item" {
  role       = aws_iam_role.delete_goal.name
  policy_arn = aws_iam_policy.DynamoDB_DeleteItem.arn
}
resource "aws_iam_role_policy_attachment" "delete_goal_basic_execution" {
  role       = aws_iam_role.delete_goal.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "delete_income" {
  name               = "delete_income_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "delete_income_delete_item" {
  role       = aws_iam_role.delete_income.name
  policy_arn = aws_iam_policy.DynamoDB_DeleteItem.arn
}
resource "aws_iam_role_policy_attachment" "delete_income_basic_execution" {
  role       = aws_iam_role.delete_income.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "edit_budget" {
  name               = "edit_budget_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "edit_budget_update_item" {
  role       = aws_iam_role.edit_budget.name
  policy_arn = aws_iam_policy.DynamoDB_UpdateItem.arn
}
resource "aws_iam_role_policy_attachment" "edit_budget_basic_execution" {
  role       = aws_iam_role.edit_budget.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}


resource "aws_iam_role" "edit_expense" {
  name               = "edit_expense_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "edit_expense_update_item" {
  role       = aws_iam_role.edit_expense.name
  policy_arn = aws_iam_policy.DynamoDB_UpdateItem.arn
}
resource "aws_iam_role_policy_attachment" "edit_expense_basic_execution" {
  role       = aws_iam_role.edit_expense.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "edit_goal" {
  name               = "edit_goal_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "edit_goal_update_item" {
  role       = aws_iam_role.edit_goal.name
  policy_arn = aws_iam_policy.DynamoDB_UpdateItem.arn
}
resource "aws_iam_role_policy_attachment" "edit_goal_basic_execution" {
  role       = aws_iam_role.edit_goal.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "edit_income" {
  name               = "edit_income_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "edit_income_update_item" {
  role       = aws_iam_role.edit_income.name
  policy_arn = aws_iam_policy.DynamoDB_UpdateItem.arn
}
resource "aws_iam_role_policy_attachment" "edit_income_basic_execution" {
  role       = aws_iam_role.edit_income.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "get_budget_status" {
  name               = "get_budget_status_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "get_budget_status_get_item" {
  role       = aws_iam_role.get_budget_status.name
  policy_arn = aws_iam_policy.DynamoDB_GetItem.arn
}
resource "aws_iam_role_policy_attachment" "get_budget_status_query_item" {
  role       = aws_iam_role.get_budget_status.name
  policy_arn = aws_iam_policy.DynamoDB_QueryItem.arn
}
resource "aws_iam_role_policy_attachment" "get_budget_status_basic_execution" {
  role       = aws_iam_role.get_budget_status.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "get_budgets" {
  name               = "get_budgets_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "get_budgets_query_item" {
  role       = aws_iam_role.get_budgets.name
  policy_arn = aws_iam_policy.DynamoDB_QueryItem.arn
}
resource "aws_iam_role_policy_attachment" "get_budgets_basic_execution" {
  role       = aws_iam_role.get_budgets.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "get_goals" {
  name               = "get_goals_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "get_goals_query_item" {
  role       = aws_iam_role.get_goals.name
  policy_arn = aws_iam_policy.DynamoDB_QueryItem.arn
}
resource "aws_iam_role_policy_attachment" "get_goals_basic_execution" {
  role       = aws_iam_role.get_goals.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "get_incomes" {
  name               = "get_incomes_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "get_incomes_query_item" {
  role       = aws_iam_role.get_incomes.name
  policy_arn = aws_iam_policy.DynamoDB_QueryItem.arn
}
resource "aws_iam_role_policy_attachment" "get_incomes_basic_execution" {
  role       = aws_iam_role.get_incomes.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "goal_status" {
  name               = "goal_status_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "goal_status_get_item" {
  role       = aws_iam_role.goal_status.name
  policy_arn = aws_iam_policy.DynamoDB_GetItem.arn
}
resource "aws_iam_role_policy_attachment" "goal_status_query_item" {
  role       = aws_iam_role.goal_status.name
  policy_arn = aws_iam_policy.DynamoDB_QueryItem.arn
}
resource "aws_iam_role_policy_attachment" "goal_status_basic_execution" {
  role       = aws_iam_role.goal_status.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "monthly_summary" {
  name               = "monthly_summary_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "monthly_summary_query_item" {
  role       = aws_iam_role.monthly_summary.name
  policy_arn = aws_iam_policy.DynamoDB_QueryItem.arn
}
resource "aws_iam_role_policy_attachment" "monthly_summary_basic_execution" {
  role       = aws_iam_role.monthly_summary.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "plaid_create_link_token" {
  name               = "plaid_create_link_token_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "plaid_create_link_token_ssm_get_parameter" {
  role       = aws_iam_role.plaid_create_link_token.name
  policy_arn = aws_iam_policy.SSM_GetParameter.arn
}
resource "aws_iam_role_policy_attachment" "plaid_create_link_token_basic_execution" {
  role       = aws_iam_role.plaid_create_link_token.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "plaid_exchange_link_token" {
  name               = "plaid_exchange_link_token_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "plaid_exchange_link_token_ssm_get_parameter" {
  role       = aws_iam_role.plaid_exchange_link_token.name
  policy_arn = aws_iam_policy.SSM_GetParameter.arn
}
resource "aws_iam_role_policy_attachment" "plaid_exchange_link_token_basic_execution" {
  role       = aws_iam_role.plaid_exchange_link_token.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}
resource "aws_iam_role_policy_attachment" "plaid_exchange_link_token_plaid_put_item" {
  role       = aws_iam_role.plaid_exchange_link_token.name
  policy_arn = aws_iam_policy.DynamoDB_PlaidPutItem.arn
}

resource "aws_iam_role" "plaid_sync_transactions" {
  name               = "plaid_sync_transactions_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "plaid_sync_transactions_ssm_get_parameter" {
  role       = aws_iam_role.plaid_sync_transactions.name
  policy_arn = aws_iam_policy.SSM_GetParameter.arn
}
resource "aws_iam_role_policy_attachment" "plaid_sync_transactions_basic_execution" {
  role       = aws_iam_role.plaid_sync_transactions.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}
resource "aws_iam_role_policy_attachment" "plaid_sync_transactions_plaid_get_item" {
  role       = aws_iam_role.plaid_sync_transactions.name
  policy_arn = aws_iam_policy.DynamoDB_PlaidGetItem.arn
}

resource "aws_iam_role_policy_attachment" "plaid_sync_transactions_plaid_update_item" {
  role       = aws_iam_role.plaid_sync_transactions.name
  policy_arn = aws_iam_policy.DynamoDB_PlaidUpdateItem.arn
}
resource "aws_iam_role_policy_attachment" "plaid_sync_transactions_put_item" {
  role       = aws_iam_role.plaid_sync_transactions.name
  policy_arn = aws_iam_policy.DynamoDB_PutItem.arn
}

resource "aws_iam_role" "process_recurring_income" {
  name               = "process_recurring_income_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "process_recurring_income_put_item" {
  role       = aws_iam_role.process_recurring_income.name
  policy_arn = aws_iam_policy.DynamoDB_PutItem.arn
}
resource "aws_iam_role_policy_attachment" "process_recurring_income_scan_item" {
  role       = aws_iam_role.process_recurring_income.name
  policy_arn = aws_iam_policy.DynamoDB_ScanItem.arn
}
resource "aws_iam_role_policy_attachment" "process_recurring_income_basic_execution" {
  role       = aws_iam_role.process_recurring_income.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "savings_calculator" {
  name               = "savings_calculator_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "savings_calculator_query_item" {
  role       = aws_iam_role.savings_calculator.name
  policy_arn = aws_iam_policy.DynamoDB_QueryItem.arn
}
resource "aws_iam_role_policy_attachment" "savings_calculator_basic_execution" {
  role       = aws_iam_role.savings_calculator.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "spending_by_category" {
  name               = "spending_by_category_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "spending_by_category_query_item" {
  role       = aws_iam_role.spending_by_category.name
  policy_arn = aws_iam_policy.DynamoDB_QueryItem.arn
}
resource "aws_iam_role_policy_attachment" "spending_by_category_basic_execution" {
  role       = aws_iam_role.spending_by_category.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}

resource "aws_iam_role" "spending_trend" {
  name               = "spending_trend_tf"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}
resource "aws_iam_role_policy_attachment" "spending_trend_query_item" {
  role       = aws_iam_role.spending_trend.name
  policy_arn = aws_iam_policy.DynamoDB_QueryItem.arn
}
resource "aws_iam_role_policy_attachment" "spending_trend_basic_execution" {
  role       = aws_iam_role.spending_trend.name
  policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}