# Module B boundary on Tokyo Lightsail

Purpose: lightweight, on-demand Xianyu/Goofish collection while preserving the server's primary VPN role.

## Module B may use
- TCP 18080 via systemd socket activation
- short-lived Python collector processes
- user-owned files under /home/ec2-user/module_b and the Xianyu scripts/config paths listed in the uninstall document

## Module B must not modify
- xray
- v2ray
- strongSwan/charon
- pptpd
- nginx
- SSH
- their configs, certificates, users, routes, or ports

## Resource policy
- VPN has absolute priority.
- Collector is on-demand, not a persistent scraper.
- systemd service uses low scheduling/IO priority and a memory cap.
- Avoid concurrent Xianyu searches.
- Stop extra searches on login/verification/risk-control responses.
- Current broad MacBook bridge cadence is every 15 minutes; extra narrow MacBook search is at most one per hourly global radar run.
