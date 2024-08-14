# VM bez dodatkowego dysku, tworzony, gdy add_additional_disk = false
resource "xenserver_vm" "new_vm_without_disk" {
  count          = var.add_additional_disk ? 0 : 1
  name_label     = var.new_vm_name
  template_name  = var.template_name
  static_mem_max = var.memory
  static_mem_min = var.memory
  vcpus          = var.cpus

  network_interface = [
    {
      network_uuid = var.network_uuid,
      device       = "0"
    }
  ]

  other_config = {
    "tf_created" = "true"
  }
}

# Opcjonalny zasób: dodatkowy dysk, tworzony tylko gdy add_additional_disk = true
resource "xenserver_vdi" "additional_disk" {
  count        = var.add_additional_disk ? 1 : 0
  name_label   = "${var.new_vm_name}-additional-disk"
  sr_uuid      = var.sr_uuid
  virtual_size = var.additional_disk_size
}

# VM z dodatkowym dyskiem, tworzony, gdy add_additional_disk = true
resource "xenserver_vm" "new_vm_with_disk" {
  count          = var.add_additional_disk ? 1 : 0
  name_label     = var.new_vm_name
  template_name  = var.template_name
  static_mem_max = var.memory
  static_mem_min = var.memory
  vcpus          = var.cpus

  hard_drive = [
    {
      vdi_uuid = xenserver_vdi.additional_disk[0].uuid,
      bootable = false,
      mode     = "RW"
    }
  ]

  network_interface = [
    {
      network_uuid = var.network_uuid,
      device       = "0"
    }
  ]

  other_config = {
    "tf_created" = "true"
  }
}
