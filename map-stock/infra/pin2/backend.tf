terraform {
  backend "s3"{
    bucket                 = "mundose222-mauro-a-pereira"
    # region                 = "us-east-1"  # No necesario si ya se ha declarado en el env del workflow
    key                    = "backend.tfstate"
    dynamodb_table         = "terraformstatelock"
  }
}

