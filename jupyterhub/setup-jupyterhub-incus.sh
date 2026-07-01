#!/usr/bin/env bash
set -euo pipefail

CONTAINER=jupyterhub
JUPYTERHUB_PORT=8000
VENV=/opt/jupyterhub
DATA_DIR=/srv/jupyterhub

echo "=== Launching Incus container ==="
incus launch images:ubuntu/24.04 $CONTAINER
incus exec $CONTAINER -- apt update
incus exec $CONTAINER -- apt upgrade -y

echo "=== Installing system packages ==="
incus exec $CONTAINER -- apt install -y \
  python3 python3-pip python3-venv \
  nodejs npm sqlite3 vim

echo "=== Installing configurable-http-proxy ==="
incus exec $CONTAINER -- npm install -g configurable-http-proxy

echo "=== Setting up Python virtual environment ==="
incus exec $CONTAINER -- python3 -m venv $VENV
incus exec $CONTAINER -- $VENV/bin/pip install --upgrade pip
incus exec $CONTAINER -- $VENV/bin/pip install \
  jupyterhub \
  jupyterlab \
  notebook \
  jupyterhub-nativeauthenticator

echo "=== Generating JupyterHub config ==="
incus exec $CONTAINER -- $VENV/bin/jupyterhub --generate-config -f /etc/jupyterhub/jupyterhub_config.py

# Configure basic settings
incus exec $CONTAINER -- sh -c "cat >> /etc/jupyterhub/jupyterhub_config.py << 'EOF'

# --- Custom settings ---
c.JupyterHub.bind_url = 'http://0.0.0.0:$JUPYTERHUB_PORT'
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
c.NativeAuthenticator.create_system_users = True
c.NativeAuthenticator.check_common_password = True
c.NativeAuthenticator.minimum_password_length = 8
c.JupyterHub.spawner_class = 'simple'
c.SimpleLocalProcessSpawner.home_dir_template = '/home/{username}'
EOF"

echo "=== Creating admin user ==="
incus exec $CONTAINER -- useradd -m -s /bin/bash admin
incus exec $CONTAINER -- sh -c "echo 'admin:changeme123' | chpasswd"
echo "  -> User: admin / Password: changeme123  (CHANGE IMMEDIATELY)"

echo "=== Setting up JupyterHub systemd service ==="
incus exec $CONTAINER -- sh -c "cat > /etc/systemd/system/jupyterhub.service << 'SERVICE'
[Unit]
Description=JupyterHub
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$DATA_DIR
ExecStart=$VENV/bin/jupyterhub -f /etc/jupyterhub/jupyterhub_config.py
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE"

incus exec $CONTAINER -- systemctl daemon-reload
incus exec $CONTAINER -- systemctl enable --now jupyterhub

echo "=== Adding Incus proxy device ==="
incus config device add $CONTAINER proxy-jupyterhub proxy \
  connect=tcp:127.0.0.1:$JUPYTERHUB_PORT \
  listen=tcp:0.0.0.0:$JUPYTERHUB_PORT

echo "=== Status ==="
sleep 2
incus exec $CONTAINER -- systemctl status jupyterhub --no-pager

IP=$(incus list $CONTAINER --format csv -c 4 | cut -d' ' -f1)
echo ""
echo "=== Done ==="
echo "JupyterHub should be available at http://$IP:$JUPYTERHUB_PORT"
echo "Log in with: admin / changeme123"
