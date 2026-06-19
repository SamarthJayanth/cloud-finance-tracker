resource "aws_iam_policy" "DynamoDB_DeleteItem" {
  name        = "DynamoDB_DeleteItem"
  path        = "/"
  description = "Allows access to delete item in incomes, expenses,budgets, and goals tables"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:DeleteItem",
        ]
        Effect   = "Allow"
        "Resource": [
                "arn:aws:dynamodb:${var.aws_region}:${aws_account_id}:table/budgets",
                "arn:aws:dynamodb:${var.aws_region}:${aws_account_id}:table/expenses",
                "arn:aws:dynamodb:${var.aws_region}:${aws_account_id}:table/goals",
                "arn:aws:dynamodb:${var.aws_region}:${aws_account_id}:table/incomes",
            ]
      },
    ]
  })
}