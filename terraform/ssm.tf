resource "aws_ssm_parameter" "plaid_client_id" {
  name  = "/cloud-finance-tracker/plaid/client_id"
  type  = "SecureString"
  value = var.plaid_client_id
}
resource "aws_ssm_parameter" "plaid_secret" {
  name  = "/cloud-finance-tracker/plaid/secret"
  type  = "SecureString"
  value = var.plaid_secret
}