from typing import Any, Optional
from pathlib import Path

import requests
from requests.exceptions import RequestException

from helpers.utils import scripts
from helpers.logger import Logger, bold

log: Logger = Logger()

def execute_event(driver: Any, event: str, command: dict[str, Any]) -> None:
    try:
        driver.execute_cdp_cmd(event, command)
        log.info(f"Executed event {bold(event)}.")
    except Exception as error:
        log.failure(
            f"Couldn't execute event {bold(event)}. Exception: {bold(str(error))}."
        )

def load_javascript_file(file_path: str, edit: bool = True) -> str:
    js_path = Path(file_path)
    if not js_path.exists():
        raise FileNotFoundError(f"JavaScript file not found: {file_path}")
    
    try:
        with js_path.open(encoding="utf-8") as file:
            source = file.read()
        
        if edit:
            return f"({source})()"
        return source
    except IOError as error:
        raise IOError(f"Could not read JavaScript file {file_path}: {error}") from error


def load_spoofing_script(driver: Any, device: Any):
    script_files = [
        scripts.utils,
        scripts.chrome_app,
        scripts.spoof,
    ]
    
    for file_path in script_files:
        execute_event(
            driver,
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": load_javascript_file(file_path)}
        )

    script = f"""
(() => {{
    Object.defineProperty(Object.getPrototypeOf(navigator), "userAgent", {{get: () => "{device.user_agent}"}})
    Object.defineProperty(Object.getPrototypeOf(navigator), "appVersion", {{get: () => "{device.user_agent.split('Mozilla/')[1] if 'Mozilla/' in device.user_agent else ''}"}})
    Object.defineProperty(Object.getPrototypeOf(navigator), "hardwareConcurrency", {{get: () => {device.hardware_concurrency}}})
    Object.defineProperty(Object.getPrototypeOf(navigator), "maxTouchPoints", {{get: () => {device.max_touch_points}}})
    Object.defineProperty(Object.getPrototypeOf(navigator), "language", {{get: () => "{device.languages}"}})
}})()
""".strip()

    execute_event(
        driver,
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": script}
    )


def get_coordinates(proxies: dict[str, str]) -> tuple[Optional[float], Optional[float]]:
    try:
        response = requests.get(
            "https://ipwho.is/",
            proxies=proxies,
            timeout=5.0
        )
        response.raise_for_status()
        obj = response.json()
        return obj.get("latitude"), obj.get("longitude")
    except (RequestException, KeyError, ValueError) as error:
        log.warning(f"Could not get coordinates: {error}")
        return None, None

def set_geolocation(driver: Any, proxies: dict[str, str]):
    latitude, longitude = get_coordinates(proxies)

    if latitude is not None and longitude is not None:
        log.info("Overriding geolocation.")
        execute_event(
            driver,
            "Emulation.setGeolocationOverride",
            {
                "latitude": latitude,
                "longitude": longitude,
                "accuracy": 100
            }
        )

def set_user_agent_metadata(driver: Any, device: Any):
    try:
        platform_version = device.user_agent.split("iPhone OS ")[1].split(" ")[0].replace("_", ".")
    except (IndexError, AttributeError):
        platform_version = "17.0"
    
    execute_event(
        driver,
        "Network.setUserAgentOverride",
        {
            "userAgent": device.user_agent,
            "userAgentMetadata": {
                "brands": [],
                "fullVersionList": [],
                "platform": "iOS",
                "platformVersion": platform_version,
                "architecture": "-",
                "model": "iPhone",
                "mobile": True,
                "bitness": "64",
                "wow64": False
            }
        }
    )

def set_canvas_fingerprint(driver: Any):
    execute_event(
        driver,
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": load_javascript_file(scripts.canvas, edit=False)}
    )

def set_audio_fingerprint(driver: Any):
    execute_event(
        driver,
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": load_javascript_file(scripts.audio, edit=False)}
    )

def load_stealth_script(driver: Any):
    execute_event(
        driver,
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": load_javascript_file(scripts.stealth_min)}
    )

def set_focus_emulation(driver: Any):
    execute_event(
        driver,
        "Emulation.setFocusEmulationEnabled",
        {"enabled": True}
    )

def set_network_enable(driver: Any):
    execute_event(driver, "Network.enable", {})

def set_mobile_metrics(driver: Any, device: Any):
    execute_event(
        driver,
        "Emulation.setDeviceMetricsOverride",
        {
            "width": device.width,
            "height": device.height,
            "deviceScaleFactor": device.device_scale_factor,
            "mobile": device.mobile
        }
    )

def set_idle_override(driver: Any, device: Any):
    execute_event(
        driver,
        "Emulation.setIdleOverride",
        {
            "isUserActive": device.touch,
            "isScreenUnlocked": device.touch
        }
    )

def set_touch_points(driver: Any, device: Any):
    execute_event(
        driver,
        "Emulation.setTouchEmulationEnabled",
        {
            "enabled": device.touch,
            "maxTouchPoints": device.max_touch_points
        }
    )

def set_touch_mode(driver: Any, device: Any):
    execute_event(
        driver,
        "Page.setTouchEmulationEnabled",
        {"enabled": device.touch}
    )

def set_blocked_urls(driver: Any, urls: list[str]):
    execute_event(
        driver,
        "Network.setBlockedURLs",
        {"urls": urls}
    )

def set_dark_mode(driver: Any, device: Any):
    execute_event(
        driver,
        "Emulation.setAutoDarkModeOverride",
        {"enabled": device.dark_mode}
    )

def set_cores(driver: Any, device: Any) -> None:
    execute_event(
        driver,
        "Emulation.setHardwareConcurrencyOverride",
        {"hardwareConcurrency": device.hardware_concurrency}
    )

def set_fake_webrtc(driver: Any) -> None:
    script = (
        "navigator.mediaDevices.getUserMedia = "
        "navigator.webkitGetUserMedia = "
        "navigator.mozGetUserMedia = "
        "navigator.getUserMedia = "
        "webkitRTCPeerConnection = "
        "RTCPeerConnection = "
        "MediaStreamTrack = undefined;"
    )
    execute_event(
        driver,
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": script}
    )
