resource "aws_dynamodb_table" "expenses" {
  name           = "expenses"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"
  range_key      = "item_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "item_id"
    type = "S"
  }
}
resource "aws_dynamodb_table" "budgets" {
  name           = "budgets"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"
  range_key      = "item_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "item_id"
    type = "S"
  }
}
resource "aws_dynamodb_table" "incomes" {
  name           = "incomes"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"
  range_key      = "item_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "item_id"
    type = "S"
  }
}
resource "aws_dynamodb_table" "goals" {
  name           = "goals"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"
  range_key      = "item_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "item_id"
    type = "S"
  }
}
resource "aws_dynamodb_table" "plaid_items" {
  name           = "plaid-items"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }
}