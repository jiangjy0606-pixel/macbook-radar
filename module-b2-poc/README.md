# Module B2 — Xianyu Browser Acceptance PoC

This branch is intentionally isolated from the existing Module B workflows.

## Goal
Test only whether a persistent GitHub Codespace can run **headed Google Chrome** and reach Goofish normally. It does not call MTOP, scrape listings, bypass CAPTCHA, schedule polling, or touch the Tokyo VPN server / BE7000.

## Create the Codespace
Create a Codespace from branch `module-b2-poc` and select the dev-container configuration:

`.devcontainer/module-b2-poc/devcontainer.json`

Use the smallest available 2-core Codespace.

## From a phone
After setup finishes, open the Codespace **Ports** view and open port **6080** (Module B2 noVNC). Keep it private. This shows the headed Linux desktop/Chrome session.

## Run L0
In the Codespace terminal:

```bash
python module-b2-poc/browser_acceptance.py
```

The test opens Goofish in real Google Chrome using a persistent profile at:

`~/.xianyu-b2/chrome-profile`

It classifies the page as `NORMAL`, `LOGIN_REQUIRED`, `BLOCKED`, or `ERROR`.

If Goofish requests a legitimate QR/login verification, complete it manually in the noVNC browser. The script deliberately does not bypass challenges.

## Privacy
Never commit `~/.xianyu-b2`, Chrome profiles, cookies, storage state, QR data, or Tailscale credentials. The repository result contains only diagnostic status, URL/title and HTTP status.

## Decision
- NORMAL / LOGIN_REQUIRED: proceed to interactive login/search acceptance.
- BLOCKED: keep the same Codespace/profile and test L1 through the home-network exit.
- ERROR: fix browser/container startup before touching networking.
