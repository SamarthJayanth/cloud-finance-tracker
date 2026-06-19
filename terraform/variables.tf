variable "aws_account_id" {
  type      = string
  sensitive = true
}
variable "aws_region" {
  type    = string
  default = "us-west-1"
}