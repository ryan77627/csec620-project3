terraform {
    required_providers {
        libvirt = {
            source = "dmacvicar/libvirt"
        }
    }
}

locals {
    ubuntu_servers = 4
    ubuntu_c2s = 3
    total_linux = 7 # MUST BE TOTAL OF UBUNTU_SERVERS AND UBUNTU_C2S!!!
    windows_client_count = 3
    windows_server_count = 1
}

provider "libvirt" {
    uri = "qemu:///system"
}

# Subnet definition
resource "libvirt_network" "main_network" {
    name = "main_net"
    addresses = ["192.168.105.0/24"]
}

# Storage Pools
resource "libvirt_pool" "main_linux_pool" {
    name = "main_linux_pool"
    type = "dir"
    target {
        path = "/csec620/terraform/ubuntu"
    }
}

resource "libvirt_pool" "main_windows_pool" {
    name = "main_windows_pool"
    type = "dir"
    target {
        path = "/csec620/terraform/windows"
    }
}

# Base Images/Install ISOs
resource "libvirt_volume" "ubuntu-base" {
    name = "ubuntu-base"
    pool = libvirt_pool.main_linux_pool.name
    source = "https://cloud-images.ubuntu.com/noble/20241004/noble-server-cloudimg-amd64.img"
    format = "qcow2"
}

# Actual disks attached to clients
resource "libvirt_volume" "ubuntu-disks" {
    name = "ubuntu-system-${count.index}.qcow2"
    pool = libvirt_pool.main_linux_pool.name
    base_volume_id = libvirt_volume.ubuntu-base.id
    count = local.total_linux
    size = 15 * 1024 * 1024 * 1024  #15GiB
}

resource "libvirt_volume" "windows-clients" {
    name = "windows-client-${count.index}.qcow2"
    pool = libvirt_pool.main_windows_pool.name
    count = local.windows_client_count
    size = 30 * 1024 * 1024 * 1024 #30GiB
}

resource "libvirt_volume" "windows-servers" {
    name = "windows-server-${count.index}.qcow2"
    pool = libvirt_pool.main_windows_pool.name
    count = local.windows_server_count
    size = 45 * 1024 * 1024 * 1024 #45GiB
}

# Ubuntu cloud init definition
data "template_file" "user_data" {
    template = file("${path.module}/ubuntu_init.cfg")
}

data "template_file" "network_config" {
    count = local.total_linux
    template = file("${path.module}/ubuntu_net.cfg")
    vars = {
        ip_address = "192.168.105.${count.index + 50}"
    }
}

# Dynamically created iso containing rendered cloudinit files
resource "libvirt_cloudinit_disk" "ubuntuinit" {
    count = local.total_linux
    name = "ubuntuinit-${count.index}.iso"
    user_data = data.template_file.user_data.rendered
    network_config = data.template_file.network_config[count.index].rendered
    pool = libvirt_pool.main_linux_pool.name
}

# Actual Virtual Machines
resource "libvirt_domain" "ubuntu-servers" {
    name = "ubuntu-server-${count.index}"
    disk {
        volume_id = libvirt_volume.ubuntu-disks[count.index].id
    }
    count = local.ubuntu_servers
    vcpu = 2
    memory = "2048"
    cloudinit = libvirt_cloudinit_disk.ubuntuinit[count.index].id
    autostart = false
    running = false

    network_interface {
        network_name = libvirt_network.main_network.name
    }

    console {
        type = "pty"
        target_port = "0"
        target_type = "serial"
    }
    
    console {
        type = "pty"
        target_port = "1"
        target_type = "virtio"
    }

    graphics {
        type = "spice"
        listen_type = "address"
        autoport = true
    }
}

resource "libvirt_domain" "windows-clients" {
    name = "windows-client-${count.index}"
    # Enable UEFI for windows
    machine = "q35"
    firmware = "/usr/share/OVMF/OVMF_CODE.fd"
    autostart = "false"
    lifecycle {
        ignore_changes = [
            nvram
        ]
    }

    # Main storage
    disk {
        volume_id = libvirt_volume.windows-clients[count.index].id
    }

    # Installation media
    disk {
        file = "${abspath(path.module)}/Win10_autoboot_installer.iso"
    }

    # Unattend media
    disk {
        file = "${abspath(path.module)}/unattend.iso"
    }

    # Virtio drivers (mostly for dynamic screen scaling when working in the VMs)
    # These are autoinstalled on first boot after installation
    disk {
        file = "${abspath(path.module)}/virtio-win-0.1.262.iso"
    }

    boot_device {
        dev = [ "hd","cdrom" ]
    }

    count = local.windows_client_count
    vcpu = 2
    memory = "4096"
    
    network_interface {
        network_name = libvirt_network.main_network.name
        addresses = [ "192.168.105.${count.index + 100}" ]
    }

    graphics {
        type = "spice"
        listen_type = "address"
        autoport = true
    }

    video {
        type = "qxl"
    }

    # Apply XSL patch to change disk types to SCSI and add tablet cursor
    xml {
        xslt = file("${path.module}/windows-patches.xsl")
    }
}

resource "libvirt_domain" "windows-servers" {
    name = "windows-server-${count.index}"
    # Enable UEFI for windows
    machine = "q35"
    firmware = "/usr/share/OVMF/OVMF_CODE.fd"
    autostart = "false"
    lifecycle {
        ignore_changes = [
            nvram
        ]
    }

    # Main storage
    disk {
        volume_id = libvirt_volume.windows-servers[count.index].id
    }

    # Installation media
    disk {
        file = "${abspath(path.module)}/WinServ2022_autoboot_installer.iso"
    }

    # Unattend media (not working for server)
    #disk {
    #    file = "${abspath(path.module)}/server_unattend.iso"
    #}

    # Virtio drivers (mostly for dynamic screen scaling when working in the VMs)
    # These are autoinstalled on first boot after installation
    disk {
        file = "${abspath(path.module)}/virtio-win-0.1.262.iso"
    }

    boot_device {
        dev = [ "hd","cdrom" ]
    }

    count = local.windows_server_count
    vcpu = 4
    memory = "6144"
    
    network_interface {
        network_name = libvirt_network.main_network.name
        addresses = [ "192.168.105.2" ] # Hardcoded for now. CHANGE ME if deploying more servers
    }

    graphics {
        type = "spice"
        listen_type = "address"
        autoport = true
    }

    video {
        type = "qxl"
    }

    # Apply XSL patch to change disk types to SCSI and add tablet cursor
    xml {
        xslt = file("${path.module}/windows-patches.xsl")
    }
}

resource "libvirt_domain" "ubuntu-c2s" {
    name = "ubuntu-c2-${count.index}"
    disk {
        volume_id = libvirt_volume.ubuntu-disks[count.index + local.ubuntu_servers].id
    }
    count = local.ubuntu_c2s
    vcpu = 2
    memory = "1512"
    cloudinit = libvirt_cloudinit_disk.ubuntuinit[count.index + local.ubuntu_servers].id
    autostart = false
    running = false

    network_interface {
        network_name = libvirt_network.main_network.name
    }

    console {
        type = "pty"
        target_port = "0"
        target_type = "serial"
    }
    
    console {
        type = "pty"
        target_port = "1"
        target_type = "virtio"
    }

    graphics {
        type = "spice"
        listen_type = "address"
        autoport = true
    }
}

# vim: set ts=4 sts=4 sw=4 et:
