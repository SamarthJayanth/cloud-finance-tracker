resource "aws_s3_bucket" "finance_tracker_frontend" {
  bucket = "finance-tracker-frontend-tf"
  # Default private, but we need to deny access specifically below
}
resource "aws_s3_bucket_public_access_block" "finance_tracker_frontend" {
  bucket = aws_s3_bucket.finance_tracker_frontend.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
# This is how cloudfront will access the s3 bucket through bucket policy

resource "aws_s3_bucket_ownership_controls" "finance_tracker_frontend" {
  bucket = aws_s3_bucket.finance_tracker_frontend.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
  # For uploaded files, the bucket owner holds ownership for all files
  # This also sets up utilizing a bucket policy
}
data "aws_iam_policy_document" "finance_tracker_frontend" {
  statement {
    principals {
        type        = "Service"
        identifiers = ["cloudfront.amazonaws.com"]
    }
    actions = [
      "s3:GetObject",
    ]

    resources = [
      "${aws_s3_bucket.finance_tracker_frontend.arn}/*",
    ]
    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.finance_tracker.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "finance_tracker_frontend" {
  bucket = aws_s3_bucket.finance_tracker_frontend.id
  policy = data.aws_iam_policy_document.finance_tracker_frontend.json
}