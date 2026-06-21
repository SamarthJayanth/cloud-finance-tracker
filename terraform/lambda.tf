# In order to make the lambda functions, we must zip them up
# We use terraform's archive file feature to do this

# We need to package the layer
# Package the Lambda function code
# And assign the role and configuration details of the function

data "archive_file" "shared_layer" {
  type        = "zip"
  source_dir  = "${path.module}/../backend/shared"
  output_path = "${path.module}/lambda_packages/shared_layer_tf.zip"
}

data "archive_file" "add_budget" {
  type        = "zip"
  # path.module is the current file path, where this code lives
  source_dir = "${path.module}/../backend/functions/add-budget"
  output_path = "${path.module}/lambda_packages/add_budget.zip"
}

resource "aws_lambda_layer_version" "shared_layer" {
  filename            = data.archive_file.shared_layer.output_path
  layer_name          = "cloud-finance-shared-tf"
  description         = "All shared utilities for cloud finance tracker"
  compatible_runtimes = ["python3.14"]
  source_code_hash    = data.archive_file.shared_layer.output_base64sha256
}

# Lambda function
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