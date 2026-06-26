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
  integration_http_method = each.value.http_method
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

