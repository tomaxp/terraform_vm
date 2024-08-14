output "vm_id" {
  value = var.add_additional_disk ? xenserver_vm.new_vm_with_disk[0].id : xenserver_vm.new_vm_without_disk[0].id
}
