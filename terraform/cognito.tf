resource "aws_cognito_user_pool" "main_pool" {
  name = "cloud-finance-tracker-pool-tf"
}
resource "aws_cognito_user_pool_client" "main_client" {
  name                 = "cloud-finance-tracker-client-tf"
  user_pool_id         = aws_cognito_user_pool.main_pool.id
  explicit_auth_flows  = ["ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"]
  generate_secret      = false
}