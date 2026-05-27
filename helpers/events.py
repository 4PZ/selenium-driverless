from typing import Any
from pathlib import Path

try:
    from .logger     import Logger, bold
    from .utils      import directories
except ImportError:
    from helpers.logger import Logger, bold
    from helpers.utils  import directories

log: Logger = Logger(prefix = "Browser")

def execute_event(driver: Any, event: str, command: dict[str, Any]) -> None:
    try:
        driver.execute_cdp_cmd(event, command)
        log.info(f"Executed event {bold(event)}")
    except Exception as error:
        log.failure(
            f"Couldn't execute event {bold(event)}. Exception: {bold(str(error))}"
        )

def load_javascript_file(file_path: str, edit: bool = True) -> str:
    js_path = Path(file_path)

    if not js_path.is_absolute():
        js_path = directories.root / file_path

    if not js_path.exists():
        raise FileNotFoundError(f"JavaScript file not found: {file_path}")

    try:
        source: str = js_path.read_text(encoding = "utf-8")
        if edit:
            return f"({source})()"
        return source
    except IOError as error:
        raise IOError(f"Could not read JavaScript file {file_path}: {error}") from error

def load_script(driver: Any, file_path: str, edit: bool = True):
    execute_event(
        driver,
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": load_javascript_file(file_path, edit = edit)}
    )

def load_scripts(driver: Any, file_paths: list[str], edit: bool = True):
    for file_path in file_paths:
        load_script(driver, file_path, edit = edit)

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
