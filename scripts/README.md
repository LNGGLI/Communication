# Local broker networking (WSL)

This file lists quick commands to:
- get the current IP inside WSL
- get the current IP on the Windows host
- create a port proxy (tunnel) from Windows → WSL so LAN devices can reach a service running in WSL2

## 1) Get the current IP in WSL
Use either of these in your WSL shell:

```bash
# preferred: shows the IP used for outgoing traffic
ip route get 1.1.1.1 | awk '{for(i=1;i<=NF;i++) if($i=="src"){print $(i+1); exit}}'

# or, show primary addresses (first IPv4)
hostname -I | awk '{print $1}'

# show full interface details
ip addr show eth0
```

Notes: On WSL2 these return the WSL VM IP (e.g. 172.x.x.x). On WSL1 the IP is the host's network stack.

## 2) Get the current IP on Windows
Open PowerShell or a Windows CMD and run one of these:

```powershell
# simple: human-readable
ipconfig

# concise: first non-169.x.x.x IPv4 address (PowerShell)
powershell -Command "Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notmatch '^169\\.'} | Select-Object -ExpandProperty IPAddress -First 1"
```

Look for the adapter that corresponds to your LAN (Ethernet or Wi‑Fi) to find the Windows machine IP.

## 3) Create a tunnel (Windows → WSL2)
When running mosquitto (or any server) inside WSL2, WSL has its own VM IP which is not reachable from other LAN devices by default. Run the following commands in an elevated (Administrator) PowerShell on Windows to forward a host port to the WSL IP.

1) Get the current WSL IP (from WSL):

```bash
# run this in WSL and copy the result to the next command
ip route get 1.1.1.1 | awk '{for(i=1;i<=NF;i++) if($i=="src"){print $(i+1); exit}}'
```

2) In an Administrator PowerShell on Windows, create the proxy (replace <WSL_IP>):

```powershell
# allow connections on all Windows interfaces to port 1883 and forward to WSL
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=1883 connectaddress=<WSL_IP> connectport=1883

# open the firewall for the port (TCP)
powershell -Command "New-NetFirewallRule -DisplayName 'MQTT WSL2' -Direction Inbound -Action Allow -Protocol TCP -LocalPort 1883"
```

3) Verify the proxy on Windows:

```powershell
netsh interface portproxy show all
```

4) To remove the forwarding rule:

```powershell
netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=1883
Remove-NetFirewallRule -DisplayName 'MQTT WSL2'
```

Notes and gotchas:
- You must run `netsh` / `New-NetFirewallRule` as Administrator.
- WSL2 IP may change after reboot or WSL restart; you must update the `connectaddress` when it changes. Consider scripting this if you restart WSL frequently.
- On WSL1 this is not required because the network is shared with Windows.
- Alternatively, run mosquitto on Windows directly or on a dedicated machine/container that binds to the LAN interface.

