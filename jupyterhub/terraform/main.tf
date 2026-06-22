data "digitalocean_ssh_key" "default" {
  name = "Richard"
}

variable "jupyterhubs" {
  default = {
    "01" = "nyc3"
    "02" = "nyc3"
  }
}

resource "digitalocean_droplet" "jupyterhub" {


  for_each = var.jupyterhubs

  name = "jupyterhub-${each.key}"

  region = each.value

  size   = "s-1vcpu-2gb"

  image  = "ubuntu-24-04-x64"

  ssh_keys = [
    data.digitalocean_ssh_key.default.id
  ]

  user_data = <<-EOF
    #cloud-config
    users:
      - name: richard
        gecos: Richard
        shell: /bin/bash
        sudo: ALL=(ALL) NOPASSWD:ALL
        groups: [sudo]
        lock_passwd: false
        ssh_authorized_keys:
          - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCkOYENzAMQR0kjNFPQpxVjUplKja+wMZbHozSjhK35p8YRLCBhu5DiS/W5kUwbOHqFBreh+mgsG4b2TpjuPtLiqhWAsCgoAyzcQYA6pmhqa5bjhZ5CFfzOfpumfeMoImD5KSQzdQtc6opfFx6/OiOi94ws9QGgf8N/ysWnJHOsDLna+Ha1qkq4lO80BrVAaybxwstKxyz8fFVcZjaA5/XRXZNR3NZFqGtOcJ30n2o6+AKaoxawX2pDr/Oy7vsW3/6uhBGXBr51j7R8ZWE9P9LqxL2lePIulh+YLmdFDQgpVzOCCq+B3WyiVkOKGATcZbFBiSl0GfSUHRF2czR1vpk+pXOGvJ730iMxgmqBpPPKUDieD/171I8Cx5RNcsdvBKc3S+nxbwn1wOhsRGFJxuD1rhrXlexDA/hUUnuV2ccwr3P9yGjW8p4zABJTNMcbnT87Ti3Jh4lAmIB0S6LRv3hLrprZpeiv20rIGBr2lVpqpAcOWXqosbIsmNfQLZxVabU= Richard@flightsim
          #- ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExamplePublicKeyReplaceWithYourOwnKeyHere user@example
  EOF
}


output "ip" {
  value = {
    for name, droplet in digitalocean_droplet.jupyterhub :
    name => droplet.ipv4_address
  }
}