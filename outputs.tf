output "vm_id" {
  value = var.add_additional_disk ? xenserver_vm.new_vm_with_disk[0].id : xenserver_vm.new_vm_without_disk[0].id
}

output "vm_mac_address" {
  value = var.add_additional_disk ? tolist(xenserver_vm.new_vm_with_disk[0].network_interface)[0].mac : tolist(xenserver_vm.new_vm_without_disk[0].network_interface)[0].mac
}

output "new_vm_name" {
  value = xenserver_vm.new_vm_without_disk[0].name_label
}

output "template_name" {
  value = xenserver_vm.new_vm_without_disk[0].template_name
}

output "memory" {
  value = xenserver_vm.new_vm_without_disk[0].static_mem_max
}

output "cpus" {
  value = xenserver_vm.new_vm_without_disk[0].vcpus
}

output "disk_size" {
  value = var.additional_disk_size
}

