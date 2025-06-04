terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

resource "aws_s3_bucket" "terraform_state_bucket" {
  bucket = "mundose222-mauro-a-pereira"
}

resource "aws_dynamodb_table" "terraform_lock_table" {
  name         = "terraformstatelock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }

  timeouts {
    create = "5m"
  }
}
