#!/usr/bin/env python3
import json, os, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

HOME = Path.home()
STATE = HOME / ".xianyu-b2"
PROFILE = STATE / "chrome-profile"
RESULTS = STATE / "results"
REPO_RESULT = Path("module-b2-poc/browser-acceptance-result.json")
PROFILE.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)

URL = "https://www.goofish.com/"
DISPLAY = os.environ.get("DISPLAY") or ":1"
os.environ["DISPLAY"] = DISPLAY

challenge_terms = ["非法访问", "正常浏览器访问", "验证码", "安全验证", "访问异常"]
login_terms = ["登录", "扫码登录", "短信登录"]

result = {
    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    "target": URL,
    "browser": "google-chrome",
    "headless": False,
    "display": DISPLAY,
    "status": "ERROR",
    "http_status": None,
    "final_url": None,
    "title": None,
    "challenge": False,
    "login_required": None,
    "note": None
}

def display_ready():
    try:
        subprocess.run(
            ["xdpyinfo", "-display", DISPLAY],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
            check=True,
        )
        return True
    except Exception:
        return False

def ensure_desktop():
    if display_ready():
        return True
    init = Path("/usr/local/share/desktop-init.sh")
    if init.exists():
        env = os.environ.copy()
        env["DISPLAY"] = DISPLAY
        try:
            subprocess.run(
                [str(init), "true"],
                env=env,
                stdout=(RESULTS / "desktop-init.log").open("w"),
                stderr=subprocess.STDOUT,
                timeout=20,
                check=False,
            )
        except Exception:
            pass
    for _ in range(15):
        if display_ready():
            return True
        time.sleep(1)
    return False

if not ensure_desktop():
    result["status"] = "DESKTOP_ERROR"
    result["note"] = (
        f"No X display available on {DISPLAY}. "
        "The desktop-lite service did not start; see ~/.xianyu-b2/results/desktop-init.log."
    )
else:
    try:
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(PROFILE),
                channel="chrome",
                headless=False,
                viewport={"width": 1280, "height": 800},
                args=["--disable-dev-shm-usage"],
            )
            page = context.pages[0] if context.pages else context.new_page()
            response = page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            time.sleep(8)
            body = page.locator("body").inner_text(timeout=15000)
            title = page.title()
            final_url = page.url
            challenge = any(x in body for x in challenge_terms)
            login_required = any(x in body for x in login_terms)
            result.update({
                "http_status": response.status if response else None,
                "final_url": final_url,
                "title": title,
                "challenge": challenge,
                "login_required": login_required,
                "status": "BLOCKED" if challenge else ("LOGIN_REQUIRED" if login_required else "NORMAL"),
                "note": "No CAPTCHA or challenge bypass is attempted. Complete any legitimate login manually in the noVNC Chrome window."
            })
            page.screenshot(path=str(RESULTS / "latest.png"), full_page=False)
            time.sleep(15)
            context.close()
    except Exception as e:
        result["note"] = f"{type(e).__name__}: {e}"

RESULTS.joinpath("browser-acceptance-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
REPO_RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
