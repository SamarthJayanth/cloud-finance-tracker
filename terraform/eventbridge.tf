resource "aws_cloudwatch_event_rule" "process_recurring_income" {
  name        = "process-recurring-income-daily-tf"
  description = "Triggers lambda process_recurring_income daily"
  schedule_expression = "cron(0 0 * * ? *)"

}
resource "aws_cloudwatch_event_target" "lambda_process_recurring_income" {
  rule      = aws_cloudwatch_event_rule.process_recurring_income.name
  target_id = "process-recurring-income-tf"
  arn       = aws_lambda_function.process_recurring_income.arn
}
resource "aws_lambda_permission" "allow_eventbridge_process_recurring_income" {
  statement_id  = "AllowEventBridgeInvokeRecurringIncome"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.process_recurring_income.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.process_recurring_income.arn
}

resource "aws_cloudwatch_event_rule" "budget_alert" {
  name        = "budget-alert-daily-tf"
  description = "Triggers lambda budget_alert daily"
  schedule_expression = "cron(0 0 * * ? *)"

}
resource "aws_cloudwatch_event_target" "lambda_budget_alert" {
  rule      = aws_cloudwatch_event_rule.budget_alert.name
  target_id = "budget-alert-tf"
  arn       = aws_lambda_function.budget_alert.arn
}
resource "aws_lambda_permission" "allow_eventbridge_budget_alert" {
  statement_id  = "AllowEventBridgeInvokeBudgetAlert"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.budget_alert.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.budget_alert.arn
}