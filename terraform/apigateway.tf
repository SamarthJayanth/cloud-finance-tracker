# We need to define our main api
# Then each resource under the api for each lambda function
# Each resource needs to have an OPTIONS method and another
# We need to specify authorizor and method types

# As there are many resources to be defined for api_gateway
# We can utilize a for each loop to help define those resources

# This will have the local variables that we can access in our set up
# This will have the necessary function configuration data
locals {
  lambda_funcs = {
    add_budget = {http_method = "POST", path_name = "add-budget", lambda_func = aws_lambda_function.add_budget}
    add_expense = {http_method = "POST", path_name = "add-expense", lambda_func = aws_lambda_function.add_expense}
    add_goal = {http_method = "POST", path_name = "add-goal", lambda_func = aws_lambda_function.add_goal}
    add_income = {http_method = "POST", path_name = "add-income", lambda_func = aws_lambda_function.add_income}
    budget_alert = {http_method = "POST", path_name = "budget-alert", lambda_func = aws_lambda_function.budget_alert}
    daily_average = {http_method = "POST", path_name = "daily-average", lambda_func = aws_lambda_function.daily_average}
    delete_budget = {http_method = "DELETE", path_name = "delete-budget", lambda_func = aws_lambda_function.delete_budget}
    delete_expense = {http_method = "DELETE", path_name = "delete-expense", lambda_func = aws_lambda_function.delete_expense}
    delete_goal = {http_method = "DELETE", path_name = "delete-goal", lambda_func = aws_lambda_function.delete_goal}
    delete_income = {http_method = "DELETE", path_name = "delete-income", lambda_func = aws_lambda_function.delete_income}
    edit_budget = {http_method = "PATCH", path_name = "edit-budget", lambda_func = aws_lambda_function.edit_budget}
    edit_expense = {http_method = "PATCH", path_name = "edit-expense", lambda_func = aws_lambda_function.edit_expense}
    edit_goal = {http_method = "PATCH", path_name = "edit-goal", lambda_func = aws_lambda_function.edit_goal}
    edit_income = {http_method = "PATCH", path_name = "edit-income", lambda_func = aws_lambda_function.edit_income}
    get_budget_status = {http_method = "POST", path_name = "get-budget-status", lambda_func = aws_lambda_function.get_budget_status}
    get_budgets = {http_method = "POST", path_name = "get-budgets", lambda_func = aws_lambda_function.get_budgets}
    get_expenses = {http_method = "POST", path_name = "get-expenses", lambda_func = aws_lambda_function.get_expenses}
    get_goals = {http_method = "POST", path_name = "get-goals", lambda_func = aws_lambda_function.get_goals}
    goal_status = {http_method = "POST", path_name = "goal-status", lambda_func = aws_lambda_function.goal_status}
    monthly_summary = {http_method = "POST", path_name = "monthly-summary", lambda_func = aws_lambda_function.monthly_summary}
    plaid_create_link_token = {http_method = "POST", path_name = "plaid-create-link-token", lambda_func = aws_lambda_function.plaid_create_link_token}
    plaid_exchange_token = {http_method = "POST", path_name = "plaid-exchange-token", lambda_func = aws_lambda_function.plaid_exchange_token}
    plaid_sync_transactions = {http_method = "POST", path_name = "plaid-sync-transactions", lambda_func = aws_lambda_function.plaid_sync_transactions}
    savings_calculator = {http_method = "POST", path_name = "savings-calculator", lambda_func = aws_lambda_function.savings_calculator}
    spending_by_category = {http_method = "POST", path_name = "spending-by-category", lambda_func = aws_lambda_function.spending_by_category}
    spending_trend = {http_method = "POST", path_name = "spending-trend", lambda_func = aws_lambda_function.spending_trend}
  }
}
resource "aws_api_gateway_rest_api" "finance_tracker_api_tf" {
  name = "finance-tracker-api-tf"
}

resource "aws_api_gateway_authorizer" "cognito_authorizer_tf" {
  name                   = "cognito-authorizer-tf"
  #Default type is token
  # We use the user pool instead to verify 
  type = "COGNITO_USER_POOLS"
  rest_api_id            = aws_api_gateway_rest_api.finance_tracker_api_tf.id
  #Provider arns required for this type
  provider_arns = [aws_cognito_user_pool.main_pool.arn]
  identity_source = "method.request.header.Authorization"
}

resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.finance_tracker_deploy_tf.id
  rest_api_id   = aws_api_gateway_rest_api.finance_tracker_api_tf.id
  stage_name    = "dev"
}

resource "aws_api_gateway_deployment" "finance_tracker_deploy_tf" {
  rest_api_id = aws_api_gateway_rest_api.finance_tracker_api_tf.id
  # We cannot use a for_each loop here
  # For_each creates multiple of a resource, but we only have one deployment

  triggers = {
    # We trigger the deployment if there is any change to any of the specified resources
    # This is done by checking if the hash is different
    redeployment = sha1(jsonencode([
      [for k, v in aws_api_gateway_resource.lambda_resources: v.id],
      [for k, v in aws_api_gateway_method.lambda_resources_options: v.id],
      [for k, v in aws_api_gateway_integration.lambda_resources_options: v.id],
      [for k, v in aws_api_gateway_method.lambda_resources_methods: v.id],
      [for k, v in aws_api_gateway_integration.lambda_resources_methods: v.id],
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_resource" "lambda_resources" {
  for_each = local.lambda_funcs
  parent_id   = aws_api_gateway_rest_api.finance_tracker_api_tf.root_resource_id
  path_part   = each.value.path_name
  rest_api_id = aws_api_gateway_rest_api.finance_tracker_api_tf.id
}

resource "aws_api_gateway_method" "lambda_resources_options" {
  authorization = "NONE"
  http_method   = "OPTIONS"
  for_each = local.lambda_funcs
  resource_id   = aws_api_gateway_resource.lambda_resources[each.key].id
  rest_api_id   = aws_api_gateway_rest_api.finance_tracker_api_tf.id
}

resource "aws_api_gateway_integration" "lambda_resources_options" {
  for_each = local.lambda_funcs
  http_method = aws_api_gateway_method.lambda_resources_options[each.key].http_method
  resource_id = aws_api_gateway_resource.lambda_resources[each.key].id
  rest_api_id = aws_api_gateway_rest_api.finance_tracker_api_tf.id
  type        = "MOCK"
}

resource "aws_api_gateway_method" "lambda_resources_methods" {
  authorization = "COGNITO_USER_POOLS"
  for_each = local.lambda_funcs
  http_method   = each.value.http_method
  resource_id   = aws_api_gateway_resource.lambda_resources[each.key].id
  rest_api_id   = aws_api_gateway_rest_api.finance_tracker_api_tf.id
  authorizer_id    = aws_api_gateway_authorizer.cognito_authorizer_tf.id
}

resource "aws_api_gateway_integration" "lambda_resources_methods" {
  for_each = local.lambda_funcs
  http_method = aws_api_gateway_method.lambda_resources_methods[each.key].http_method
  resource_id = aws_api_gateway_resource.lambda_resources[each.key].id
  rest_api_id = aws_api_gateway_rest_api.finance_tracker_api_tf.id
  integration_http_method = "POST" # API Gateway invokes with a POST, even if the integration method is different
  type                    = "AWS_PROXY"
  uri                     = each.value.lambda_func.invoke_arn
}

resource "aws_lambda_permission" "lambda_functions_apigw" {
  for_each = local.lambda_funcs
  statement_id  = "AllowExecutionFromAPIGateway-${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = each.value.lambda_func.function_name
  principal     = "apigateway.amazonaws.com"
# Source arn from aws documentation for api gateway
  source_arn = "${aws_api_gateway_rest_api.finance_tracker_api_tf.execution_arn}/*/*"

  }

resource "aws_api_gateway_method_response" "lambda_resources_options" {
  for_each = local.lambda_funcs
  rest_api_id = aws_api_gateway_rest_api.finance_tracker_api_tf.id
  resource_id = aws_api_gateway_resource.lambda_resources[each.key].id
  http_method = aws_api_gateway_method.lambda_resources_options[each.key].http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "lambda_resources_options" {
  for_each = local.lambda_funcs
  
  rest_api_id = aws_api_gateway_rest_api.finance_tracker_api_tf.id
  resource_id = aws_api_gateway_resource.lambda_resources[each.key].id
  http_method = aws_api_gateway_method.lambda_resources_options[each.key].http_method
  status_code = aws_api_gateway_method_response.lambda_resources_options[each.key].status_code

   response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,Authorization'"
    "method.response.header.Access-Control-Allow-Methods" = "'${each.value.http_method},OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  } 
}

