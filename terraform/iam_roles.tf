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