#!/usr/bin/env bash
set -euo pipefail

echo "=== Installing Ansible and dependencies for Incus JupyterHub playbook ==="

# Detect package manager
if command -v apt &>/dev/null; then
  PKG="apt"
elif command -v dnf &>/dev/null; then
  PKG="dnf"
elif command -v yum &>/dev/null; then
  PKG="yum"
else
  echo "Unsupported package manager. Install ansible-core manually."
  exit 1
fi

# Install ansible-core if not present
if ! command -v ansible &>/dev/null; then
  echo "--- Installing ansible-core ---"
  case "$PKG" in
    apt) sudo apt update && sudo apt install -y ansible-core ;;
    dnf) sudo dnf install -y ansible-core ;;
    yum) sudo yum install -y ansible-core ;;
  esac
fi

echo "--- Installing community.general collection ---"
ansible-galaxy collection install community.general

# Verify the lxd_container module is available
echo "--- Verifying lxd_container module ---"
ansible-doc -t module community.general.lxd_container &>/dev/null \
  && echo "OK: lxd_container module is available" \
  || echo "WARNING: lxd_container module not found. Try: ansible-galaxy collection install community.general --force"

# Ensure Incus is installed (required on the target host)
if ! command -v incus &>/dev/null; then
  echo ""
  echo "WARNING: incus is not installed on this machine."
  echo "The playbook runs against an Incus host. Install Incus with:"
  echo "  sudo apt install incus  # Debian/Ubuntu"
  echo "  sudo dnf install incus  # Fedora"
fi

# Verify Python 3
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 is required. Install it and re-run."
  exit 1
fi

echo ""
echo "=== All dependencies installed ==="
echo "Run the playbook with:"
echo "  ansible-playbook -i <inventory> ansible/incus-jupyterhub.yml"
