from typing import Any

class button_sleep:
    general: float = 0.50
    clicked: float = 0.25
    retry:   float = 0.15
    typing:  float = 0.02
    action:  float = 0.25

def make_arguments(device: object, config: object) -> list[str]:
    disable_features: list[str] = [
        "enable-lens-region-search",
        "AutofillSaveCardBubble",
        "PasswordLeakDetection",
        "enable-client-hints",
        "SidePanelPinning",
        "UserAgentClientHint",
        "Translate",
        "PrivacySandboxSettings4",
        "InterestFeedContentSuggestions",
        "OptimizationGuideModelDownloading",
        "OptimizationHintsFetching",
        "OptimizationTargetPrediction",
        "OptimizationHints",
        "UseOsCryptAsyncForCookieEncryption",
        "PrintCompositorLPAC"
    ]

    arguments: list[str] = [
        "--disable-device-discovery-notifications",
        "--disable-password-generation",
        "--disable-single-click-autofill",
        "--ash-no-nudges",
        "--disable-background-downloads",
        "--disable-background-timer-throttling",
        "--disable-client-side-phishing-detection",
        "--disable-component-update",
        "--disable-credentials-enable-service",
        "--disable-features=" + ",".join(disable_features),
        "--disable-infobars",
        "--disable-overscroll-edge-effect",
        "--disable-password-manager-reauthentication",
        "--disable-popup-blocking",
        "--disable-renderer-backgrounding",
        "--disable-save-password-bubble",
        "--enable-font-antialiasing",
        "--enable-gpu-rasterization",
        "--hide-crash-restore-bubble",
        "--password-store=basic",
        "--use-mock-keychain",
        "--window-position=0,0"
    ]

    if getattr(config, "cache", False):
        arguments.append("--disk-cache-dir=" + str(config.cache_directory))

    if getattr(config, "profiles", False):
        arguments.append("--user-data-dir=" + str(config.profile_directory))

    for argument in ["--window-size"]:
        arguments.append(argument + "=" + ",".join([str(device.width), str(device.height + 28)]))

    for argument in ["--device-scale-factor", "--force-device-scale-factor"]:
        arguments.append(argument + "=" + str(device.device_scale_factor))

    arguments.append("--touch-events=enabled")
    arguments.append("--cast-initial-screen-width="  + str(device.width))
    arguments.append("--cast-initial-screen-height=" + str(device.height))
    arguments.append("--user-agent=" + device.user_agent)

    return arguments

def make_prefs(device: object) -> dict[str, Any]:
    return {
        "credentials_enable_service":              False,
        "intl.accept_languages":                   device.languages,
        "plugins.always_open_pdf_externally":      False,
        "profile.password_manager_enabled":        False,
        "search.suggest_enabled":                  False,
        "translate.enabled":                       False,
        "webkit.webprefs.force_dark_mode_enabled": device.dark_mode,
    }
