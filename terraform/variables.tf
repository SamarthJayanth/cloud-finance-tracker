variable "aws_account_id" {
  type      = string
  sensitive = true
}
variable "aws_region" {
  type    = string
  default = "us-west-1"
}
variable "plaid_client_id" {
  type    = string
  sensitive = true
}
variable "plaid_secret" {
  type = string
  sensitive = true
}
variable "budget_alert_email" {
  type = string
  sensitive   = true
}