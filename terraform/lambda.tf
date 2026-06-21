# In order to make the lambda functions, we must zip them up
# We use terraform's archive file feature to do this

# We need to package the layer
# Package the Lambda function code
# And assign the role and configuration details of the function

data "archive_file" "shared_layer" {
  type        = "zip"
  source_dir  = "${path.module}/../backend/shared/shared_layer"
  output_path = "${path.module}/lambda_packages/shared_layer_tf.zip"
}
resource "aws_lambda_layer_version" "shared_layer" {
  filename            = data.archive_file.shared_layer.output_path
  layer_name          = "cloud-finance-shared-tf"
  description         = "All shared utilities for cloud finance tracker"
  compatible_runtimes = ["python3.14"]
  source_code_hash    = data.archive_file.shared_layer.output_base64sha256
}

data "archive_file" "add_budget" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/add-budget"
  output_path = "${path.module}/lambda_packages/add_budget.zip"
}
resource "aws_lambda_function" "add_budget" {
  filename      = data.archive_file.add_budget.output_path
  function_name = "add_budget_tf"
  role          = aws_iam_role.add_budget.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.add_budget.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "add_expense" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/add-expense"
  output_path = "${path.module}/lambda_packages/add_expense.zip"
}
resource "aws_lambda_function" "add_expense" {
  filename      = data.archive_file.add_expense.output_path
  function_name = "add_expense_tf"
  role          = aws_iam_role.add_expense.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.add_expense.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "add_goal" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/add-goal"
  output_path = "${path.module}/lambda_packages/add_goal.zip"
}
resource "aws_lambda_function" "add_goal" {
  filename      = data.archive_file.add_goal.output_path
  function_name = "add_goal_tf"
  role          = aws_iam_role.add_goal.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.add_goal.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "add_income" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/add-income"
  output_path = "${path.module}/lambda_packages/add_income.zip"
}
resource "aws_lambda_function" "add_income" {
  filename      = data.archive_file.add_income.output_path
  function_name = "add_income_tf"
  role          = aws_iam_role.add_income.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.add_income.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "budget_alert" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/budget-alert"
  output_path = "${path.module}/lambda_packages/budget_alert.zip"
}
resource "aws_lambda_function" "budget_alert" {
  filename      = data.archive_file.budget_alert.output_path
  function_name = "budget_alert_tf"
  role          = aws_iam_role.budget_alert.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.budget_alert.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "daily_average" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/daily-average"
  output_path = "${path.module}/lambda_packages/daily_average.zip"
}
resource "aws_lambda_function" "daily_average" {
  filename      = data.archive_file.daily_average.output_path
  function_name = "daily_average_tf"
  role          = aws_iam_role.daily_average.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.daily_average.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "delete_budget" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/delete-budget"
  output_path = "${path.module}/lambda_packages/delete_budget.zip"
}
resource "aws_lambda_function" "delete_budget" {
  filename      = data.archive_file.delete_budget.output_path
  function_name = "delete_budget_tf"
  role          = aws_iam_role.delete_budget.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.delete_budget.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "delete_expense" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/delete-expense"
  output_path = "${path.module}/lambda_packages/delete_expense.zip"
}
resource "aws_lambda_function" "delete_expense" {
  filename      = data.archive_file.delete_expense.output_path
  function_name = "delete_expense_tf"
  role          = aws_iam_role.delete_expense.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.delete_expense.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "delete_goal" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/delete-goal"
  output_path = "${path.module}/lambda_packages/delete_goal.zip"
}
resource "aws_lambda_function" "delete_goal" {
  filename      = data.archive_file.delete_goal.output_path
  function_name = "delete_goal_tf"
  role          = aws_iam_role.delete_goal.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.delete_goal.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "delete_income" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/delete-income"
  output_path = "${path.module}/lambda_packages/delete_income.zip"
}
resource "aws_lambda_function" "delete_income" {
  filename      = data.archive_file.delete_income.output_path
  function_name = "delete_income_tf"
  role          = aws_iam_role.delete_income.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.delete_income.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "edit_budget" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/edit-budget"
  output_path = "${path.module}/lambda_packages/edit_budget.zip"
}
resource "aws_lambda_function" "edit_budget" {
  filename      = data.archive_file.edit_budget.output_path
  function_name = "edit_budget_tf"
  role          = aws_iam_role.edit_budget.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.edit_budget.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "edit_expense" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/edit-expense"
  output_path = "${path.module}/lambda_packages/edit_expense.zip"
}
resource "aws_lambda_function" "edit_expense" {
  filename      = data.archive_file.edit_expense.output_path
  function_name = "edit_expense_tf"
  role          = aws_iam_role.edit_expense.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.edit_expense.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "edit_goal" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/edit-goal"
  output_path = "${path.module}/lambda_packages/edit_goal.zip"
}
resource "aws_lambda_function" "edit_goal" {
  filename      = data.archive_file.edit_goal.output_path
  function_name = "edit_goal_tf"
  role          = aws_iam_role.edit_goal.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.edit_goal.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "edit_income" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/edit-income"
  output_path = "${path.module}/lambda_packages/edit_income.zip"
}
resource "aws_lambda_function" "edit_income" {
  filename      = data.archive_file.edit_income.output_path
  function_name = "edit_income_tf"
  role          = aws_iam_role.edit_income.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.edit_income.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "get_budget_status" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/get-budget-status"
  output_path = "${path.module}/lambda_packages/get_budget_status.zip"
}
resource "aws_lambda_function" "get_budget_status" {
  filename      = data.archive_file.get_budget_status.output_path
  function_name = "get_budget_status_tf"
  role          = aws_iam_role.get_budget_status.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.get_budget_status.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "get_budgets" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/get-budgets"
  output_path = "${path.module}/lambda_packages/get_budgets.zip"
}
resource "aws_lambda_function" "get_budgets" {
  filename      = data.archive_file.get_budgets.output_path
  function_name = "get_budgets_tf"
  role          = aws_iam_role.get_budgets.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.get_budgets.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "get_expenses" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/get-expenses"
  output_path = "${path.module}/lambda_packages/get_expenses.zip"
}
resource "aws_lambda_function" "get_expenses" {
  filename      = data.archive_file.get_expenses.output_path
  function_name = "get_expenses_tf"
  role          = aws_iam_role.get_expenses.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.get_expenses.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "get_goals" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/get-goals"
  output_path = "${path.module}/lambda_packages/get_goals.zip"
}
resource "aws_lambda_function" "get_goals" {
  filename      = data.archive_file.get_goals.output_path
  function_name = "get_goals_tf"
  role          = aws_iam_role.get_goals.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.get_goals.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "get_incomes" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/get-incomes"
  output_path = "${path.module}/lambda_packages/get_incomes.zip"
}
resource "aws_lambda_function" "get_incomes" {
  filename      = data.archive_file.get_incomes.output_path
  function_name = "get_incomes_tf"
  role          = aws_iam_role.get_incomes.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.get_incomes.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "goal_status" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/goal-status"
  output_path = "${path.module}/lambda_packages/goal_status.zip"
}
resource "aws_lambda_function" "goal_status" {
  filename      = data.archive_file.goal_status.output_path
  function_name = "goal_status_tf"
  role          = aws_iam_role.goal_status.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.goal_status.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "monthly_summary" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/monthly-summary"
  output_path = "${path.module}/lambda_packages/monthly_summary.zip"
}
resource "aws_lambda_function" "monthly_summary" {
  filename      = data.archive_file.monthly_summary.output_path
  function_name = "monthly_summary_tf"
  role          = aws_iam_role.monthly_summary.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.monthly_summary.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "plaid_create_link_token" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/plaid-create-link-token"
  output_path = "${path.module}/lambda_packages/plaid_create_link_token.zip"
}
resource "aws_lambda_function" "plaid_create_link_token" {
  filename      = data.archive_file.plaid_create_link_token.output_path
  function_name = "plaid_create_link_token_tf"
  role          = aws_iam_role.plaid_create_link_token.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.plaid_create_link_token.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "plaid_exchange_link_token" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/plaid-exchange-link-token"
  output_path = "${path.module}/lambda_packages/plaid_exchange_link_token.zip"
}
resource "aws_lambda_function" "plaid_exchange_link_token" {
  filename      = data.archive_file.plaid_exchange_link_token.output_path
  function_name = "plaid_exchange_link_token_tf"
  role          = aws_iam_role.plaid_exchange_link_token.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.plaid_exchange_link_token.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "plaid_sync_transactions" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/plaid-sync-transactions"
  output_path = "${path.module}/lambda_packages/plaid_sync_transactions.zip"
}
resource "aws_lambda_function" "plaid_sync_transactions" {
  filename      = data.archive_file.plaid_sync_transactions.output_path
  function_name = "plaid_sync_transactions_tf"
  role          = aws_iam_role.plaid_sync_transactions.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.plaid_sync_transactions.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "process_recurring_income" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/process-recurring-income"
  output_path = "${path.module}/lambda_packages/process_recurring_income.zip"
}
resource "aws_lambda_function" "process_recurring_income" {
  filename      = data.archive_file.process_recurring_income.output_path
  function_name = "process_recurring_income_tf"
  role          = aws_iam_role.process_recurring_income.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.process_recurring_income.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "savings_calculator" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/savings-calculator"
  output_path = "${path.module}/lambda_packages/savings_calculator.zip"
}
resource "aws_lambda_function" "savings_calculator" {
  filename      = data.archive_file.savings_calculator.output_path
  function_name = "savings_calculator_tf"
  role          = aws_iam_role.savings_calculator.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.savings_calculator.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "spending_by_category" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/spending-by-category"
  output_path = "${path.module}/lambda_packages/spending_by_category.zip"
}
resource "aws_lambda_function" "spending_by_category" {
  filename      = data.archive_file.spending_by_category.output_path
  function_name = "spending_by_category_tf"
  role          = aws_iam_role.spending_by_category.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.spending_by_category.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}

data "archive_file" "spending_trend" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/spending-trend"
  output_path = "${path.module}/lambda_packages/spending_trend.zip"
}
resource "aws_lambda_function" "spending_trend" {
  filename      = data.archive_file.spending_trend.output_path
  function_name = "spending_trend_tf"
  role          = aws_iam_role.spending_trend.arn
  handler       = "lambda_function.lambda_handler"
  source_code_hash  = data.archive_file.spending_trend.output_base64sha256
  timeout =  30
  runtime = "python3.14"
  layers = [aws_lambda_layer_version.shared_layer.arn]
}