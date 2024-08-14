variable "host" {
  description = "The base URL of target XenServer host"
  type        = string
}

variable "username" {
  description = "The username for XenServer"
  type        = string
}

variable "password" {
  description = "The password for XenServer"
  type        = string
  sensitive   = true
}

variable "template_name" {
  description = "The template name to clone the VM from"
  type        = string
}

variable "new_vm_name" {
  description = "The name for the new VM"
  type        = string
}

variable "cpus" {
  description = "Number of vCPUs for the new VM"
  type        = number
}

variable "memory" {
  description = "Amount of memory (in bytes) for the new VM"
  type        = number
}

variable "network_uuid" {
  description = "The UUID of the network to attach to the VM"
  type        = string
}

variable "sr_uuid" {
  description = "The UUID of the storage repository for the VM disk"
  type        = string
}
