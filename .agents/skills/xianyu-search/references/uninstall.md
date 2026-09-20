# Xianyu Search / Module B uninstall boundary

Use this only when the user explicitly asks to remove the Xianyu search capability.

## Boundary: assets owned by this project

### Tokyo server OS-side
- /home/ec2-user/module_b/
- /home/ec2-user/xianyu_search.py
- /home/ec2-user/xianyu_collect.py
- /home/ec2-user/.config/module_b/
- /home/ec2-user/.config/xianyu/cookie.txt
- /etc/systemd/system/module-b.socket
- /etc/systemd/system/module-b@.service
- systemd symlinks created for module-b.socket

Possible project backups with these exact prefixes may also be removed:
- /home/ec2-user/xianyu_search.py.WORKING*
- /home/ec2-user/module_b/*.WORKING*
- /home/ec2-user/module_b/*.bak*

### AWS edge resources created for Module B
- CloudFront distribution: EUCUTI4IFG9R
- CloudFront hostname: d3uiiydii9q99b.cloudfront.net
- API Gateway v2 API: 0pf6fb19dl
- earlier unused API Gateway API: vqxz9yqpe5
- Lightsail public firewall rule for TCP 18080, if it was added solely for Module B

### GitHub bridge assets
Repository: jiangjy0606-pixel/macbook-radar
Project-owned paths include:
- .agents/skills/xianyu-search/
- .github/workflows/xianyu-bridge.yml
- .github/workflows/xianyu-on-demand.yml
- request.json
- latest-query.json
- latest.json
- latest-public.json
- xianyu-state.json
- xianyu-delta.json
- server/http_trigger_v2.py
- server/refresh_mtop_token.py
- server/run_v3.sh
- server/uninstall_module_b_os.sh
- server/MODULE_B_BOUNDARY.md
- CHATGPT_XIANYU_SKILL.md

## DO NOT TOUCH

The uninstall must not stop, disable, edit, delete, or change configuration for:
- xray
- v2ray
- strongSwan / charon
- pptpd
- nginx
- SSH
- ports/services 443, 8443, 9443, 1723, UDP 500, UDP 4500
- unrelated certificates, VPN users, routes, firewall rules, or system packages

VPN has absolute priority.

## Safe removal sequence

1. Run the OS-only cleanup script:
   `sudo bash server/uninstall_module_b_os.sh`
   or copy its contents to the Tokyo host and run it there.
2. Verify VPN-related services/ports still behave as before.
3. Separately remove the Lightsail TCP 18080 firewall rule if it exists only for Module B.
4. Disable CloudFront distribution EUCUTI4IFG9R, wait until deployed/disabled, then delete it.
5. Delete API Gateway APIs 0pf6fb19dl and vqxz9yqpe5 if they are no longer needed.
6. Remove the Codex global skill directory:
   `rm -rf "$HOME/.agents/skills/xianyu-search"`
7. Optionally remove the GitHub bridge files or repository after confirming no other workflow depends on them.

Do not delete the Tokyo Lightsail instance, static IP, VPN stack, nginx, or unrelated AWS resources as part of this uninstall.
