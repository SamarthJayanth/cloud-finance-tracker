# We need to define our main api
# Then each resource under the api for each lambda function
# Each resource needs to have an OPTIONS method and another
# We need to specify authorizor and method types

# As there are many resources to be defined for api_gateway
# We can utilize a for each loop to help define those resources

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

  triggers = {
    # We trigger the deployment if there is any change to any of the specified resources
    # This is done by checking if the hash is different
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.add_budget.id,
      aws_api_gateway_method.add_budget_options.id,
      aws_api_gateway_integration.add_budget_options.id,
      aws_api_gateway_method.add_budget_post.id,
      aws_api_gateway_integration.add_budget_post.id,

    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_resource" "add_budget" {
  parent_id   = aws_api_gateway_rest_api.finance_tracker_api_tf.root_resource_id
  path_part   = "add-budget"
  rest_api_id = aws_api_gateway_rest_api.finance_tracker_api_tf.id
}

resource "aws_api_gateway_method" "add_budget_options" {
  authorization = "NONE"
  http_method   = "OPTIONS"
  resource_id   = aws_api_gateway_resource.add_budget.id
  rest_api_id   = aws_api_gateway_rest_api.finance_tracker_api_tf.id
}

resource "aws_api_gateway_integration" "add_budget_options" {
  http_method = aws_api_gateway_method.add_budget_options.http_method
  resource_id = aws_api_gateway_resource.add_budget.id
  rest_api_id = aws_api_gateway_rest_api.finance_tracker_api_tf.id
  type        = "MOCK"
}

resource "aws_api_gateway_method" "add_budget_post" {
  authorization = "COGNITO_USER_POOLS"
  http_method   = "POST"
  resource_id   = aws_api_gateway_resource.add_budget.id
  rest_api_id   = aws_api_gateway_rest_api.finance_tracker_api_tf.id
  authorizer_id    = aws_api_gateway_authorizer.cognito_authorizer_tf.id
}

resource "aws_api_gateway_integration" "add_budget_post" {
  http_method = aws_api_gateway_method.add_budget_options.http_method
  resource_id = aws_api_gateway_resource.add_budget.id
  rest_api_id = aws_api_gateway_rest_api.finance_tracker_api_tf.id
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.add_budget.invoke_arn
}

resource "aws_lambda_permission" "add_budget_apigw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.add_budget.function_name
  principal     = "apigateway.amazonaws.com"
# Source arn from aws documentation for api gateway
  source_arn = "${aws_api_gateway_rest_api.finance_tracker_api_tf.execution_arn}/*/*"

  }


