terraform {
  required_providers {
    xenserver = {
      source  = "xenserver/xenserver"
    }
  }
}

provider "xenserver" {
  host     = var.host
  username = var.username
  password = var.password
}
