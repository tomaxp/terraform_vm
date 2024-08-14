resource "xenserver_vdi" "main_disk" {
  name_label   = "${var.new_vm_name}-disk"
  sr_uuid      = var.sr_uuid
  virtual_size = 50 * 1024 * 1024 * 1024  # 50GB w bajtach
}

resource "xenserver_vm" "new_vm" {
  name_label     = var.new_vm_name
  template_name  = var.template_name
  static_mem_max = var.memory
  vcpus          = var.cpus

  # Dodajemy dysk twardy do maszyny wirtualnej
  hard_drive = [
    {
      vdi_uuid = xenserver_vdi.main_disk.uuid,
      bootable = true,
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
