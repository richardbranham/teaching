resource "digitalocean_droplet" "jupyterhub" {

  name   = "jupyterhub"
  region = "nyc3"

  size   = "s-4vcpu-8gb"

  image  = "ubuntu-24-04-x64"

  ssh_keys = [
    var.ssh_key_id
  ]
}

output "ip" {
  value = digitalocean_droplet.jupyterhub.ipv4_address
}