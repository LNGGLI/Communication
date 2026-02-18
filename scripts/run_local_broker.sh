#!/usr/bin/env bash
# Runs mosquitto in foreground using the local config in this repo.
# No sudo required when binding to port 1883 (unprivileged on many systems).
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
CFG="$HERE/mosquitto_local.conf"
echo "Starting local mosquitto with config: $CFG"#

# Try to determine the machine's local IP so users know where the broker is reachable
IP="$(ip route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i=="src"){print $(i+1); exit}}')"
if [ -z "$IP" ]; then
	IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
fi
if [ -n "$IP" ]; then
	echo "Broker will be reachable on ${IP}:1883 (local network)"
else
	echo "Could not determine local IP address; broker will bind to default interfaces"
fi

mosquitto -c "$CFG" -v
