resource "aws_iam_policy" "DynamoDB_DeleteItem" {
  name        = "DynamoDB_DeleteItem_tf"
  path        = "/"
  description = "Allows access to delete item in incomes, expenses, budgets, and goals tables"

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
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/budgets",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/expenses",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/goals",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/incomes",
            ]
      },
    ]
  })
}
resource "aws_iam_policy" "DynamoDB_GetItem" {
  name        = "DynamoDB_GetItem_tf"
  path        = "/"
  description = "Allows access to get item in incomes, expenses, budgets, and goals tables"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
        ]
        Effect   = "Allow"
        "Resource": [
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/budgets",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/expenses",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/goals",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/incomes",
            ]
      },
    ]
  })
}
resource "aws_iam_policy" "DynamoDB_PlaidGetItem" {
  name        = "DynamoDB_PlaidGetItem_tf"
  path        = "/"
  description = "Allows access to get item from plaid-items table"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
        ]
        Effect   = "Allow"
        "Resource": [
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/plaid-items",
            ]
      },
    ]
  })
}
resource "aws_iam_policy" "DynamoDB_PlaidPutItem" {
  name        = "DynamoDB_PlaidPutItem_tf"
  path        = "/"
  description = "Gives access to put item in plaid-items table"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:PutItem",
        ]
        Effect   = "Allow"
        "Resource": [
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/plaid-items",
            ]
      },
    ]
  })
}
resource "aws_iam_policy" "DynamoDB_PlaidQueryItem" {
  name        = "DynamoDB_PlaidQueryItem_tf"
  path        = "/"
  description = "Allows querying to plaid-items table in dynamodb"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:Query",
        ]
        Effect   = "Allow"
        "Resource": [
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/plaid-items",
            ]
      },
    ]
  })
}
resource "aws_iam_policy" "DynamoDB_PlaidUpdateItem" {
  name        = "DynamoDB_PlaidUpdateItem_tf"
  path        = "/"
  description = "Gives access to update an item in plaid-items table"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:UpdateItem",
        ]
        Effect   = "Allow"
        "Resource": [
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/plaid-items",
            ]
      },
    ]
  })
}
resource "aws_iam_policy" "DynamoDB_PutItem" {
  name        = "DynamoDB_PutItem_tf"
  path        = "/"
  description = "Gives access to put items in budgets, expenses, goals, incomes tables"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:PutItem",
        ]
        Effect   = "Allow"
        "Resource": [
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/budgets",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/expenses",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/goals",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/incomes",
            ]
      },
    ]
  })
}
resource "aws_iam_policy" "DynamoDB_QueryItem" {
  name        = "DynamoDB_QueryItem_tf"
  path        = "/"
  description = "Allows querying to incomes, budgets, expenses, and goals tables"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:Query",
        ]
        Effect   = "Allow"
        "Resource": [
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/budgets",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/expenses",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/goals",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/incomes",
            ]
      },
    ]
  })
}
resource "aws_iam_policy" "DynamoDB_ScanItem" {
  name        = "DynamoDB_ScanItem_tf"
  path        = "/"
  description = "Allows access to scan items in goals, expenses, budgets, incomes tables"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:Scan",
        ]
        Effect   = "Allow"
        "Resource": [
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/budgets",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/expenses",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/goals",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/incomes",
            ]
      },
    ]
  })
}
resource "aws_iam_policy" "DynamoDB_UpdateItem" {
  name        = "DynamoDB_UpdateItem_tf"
  path        = "/"
  description = "Allows access to update an item in goals, expenses, budgets, and incomes tables"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:UpdateItem",
        ]
        Effect   = "Allow"
        "Resource": [
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/budgets",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/expenses",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/goals",
                "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/incomes",
            ]
      },
    ]
  })
}
resource "aws_iam_policy" "SSM_GetParameter" {
  name        = "SSM_GetParameter_tf"
  path        = "/"
  description = "Allows access to get Plaid parameters from SSM Parameter Store"
  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ssm:GetParameter",
        ]
        Effect   = "Allow"
        "Resource": [
                "arn:aws:ssm:${var.aws_region}:${var.aws_account_id}:parameter/cloud-finance-tracker/plaid/*"
            ]
      },
    ]
  })
}
