#!/usr/bin/env bash
# Runs nats-server in foreground using the local config in this repo.
# No sudo required when binding to default port 4222.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
CFG="$HERE/nats_local.conf"
echo "Starting local nats-server with config: $CFG"#

# Try to determine the machine's local IP so users know where the broker is reachable
IP="$(ip route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i=="src"){print $(i+1); exit}}')"
if [ -z "$IP" ]; then
	IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
fi
if [ -n "$IP" ]; then
	echo "Broker will be reachable on ${IP}:4222 (local network)"
else
	echo "Could not determine local IP address; broker will bind to default interfaces"
fi

nats-server -c "$CFG" -DV  # verbose + debug

