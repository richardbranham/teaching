terraform {
  required_providers {
    proxmox = {
      source  = "telmate/proxmox"
      version = "~> 2.9"
    }
  }
}

provider "proxmox" {
  pm_api_url       = var.pm_api_url
  pm_user          = var.pm_user
  pm_password      = var.pm_password
  pm_tls_insecure  = true
}

resource "null_resource" "ensure_cloud_image" {
  triggers = {
    url  = "https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"
    dest = "/var/lib/vz/template/iso/noble-server-cloudimg-amd64.img"
  }

  provisioner "local-exec" {
    command = <<EOT
      set -e
      DEST="/var/lib/vz/template/iso/noble-server-cloudimg-amd64.img"
      [ -f "$DEST" ] && exit 0
      wget -q -O "$DEST" "https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img"
      qemu-img info "$DEST"
    EOT
  }
}

resource "proxmox_vm_qemu" "jupyterhub_01" {
  name        = "jupyterhub-01"
  vmid        = 200
  target_node = var.pm_node

  cores   = 1
  sockets = 1
  memory  = 4096

  disk {
    slot     = 0
    size     = "32G"
    type     = "virtio"
    storage  = var.pm_storage
    iothread = true
  }

  network {
    model  = "virtio"
    bridge = "vmbr1"
  }

  os_type    = "cloud-init"
  ciuser     = "richard"
  sshkeys    = file(var.ssh_public_key_path)
  ipconfig0  = "ip=10.10.10.100/24,gw=10.10.10.1"
  nameserver = "1.1.1.1"

  scsihw = "virtio-scsi-pci"
  boot   = "order=scsi0"

  depends_on = [null_resource.ensure_cloud_image]
}
