from pathlib import Path

class scripts:
    directory:   str = "data/js"
    example:     str = "data/js/example.js"
    audio:       str = "data/js/audio.js"
    canvas:      str = "data/js/canvas.js"
    chrome_app:  str = "data/js/chrome.app.js"
    gpu:         str = "data/js/gpu.js"
    spoof:       str = "data/js/spoof.js"
    stealth_min: str = "data/js/stealth.min.js"
    utils:       str = "data/js/utils.js"

class directories:
    root:        Path = Path(__file__).resolve().parent.parent
    data:        Path = root / "data"
    javascript:  Path = data / "js"
    user_agents: Path = data / "user_agents.ini"
    cache:       Path = data / "cache"
    profile:     Path = data / "profile"
