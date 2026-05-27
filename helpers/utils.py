from time           import time, sleep
from atexit         import register
from requests       import get
from subprocess     import run
from pathlib        import Path

from helpers.logger import Logger, bold

log: object = Logger()
blacklist_ = []

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

def timestamp() -> int:
    return int(time())

def exit_handler(): 
    kill_chrome_processes() 
    kill_tunnel_processes()

register(exit_handler)

def kill_chrome_processes():
    run(["pkill", "-f", "Google Chrome"])

def kill_tunnel_processes():
    run(["pkill", "-9", "python3"])

def get_ip_address(proxy: str) -> str:
    for _ in range(5):
        for url in [
            "http://ifconfig.me/ip",
            "http://wtfismyip.com/"
        ]:
            if url in blacklist_:
                continue

            try:
                response: object = get(url, proxies = {"http": proxy.replace("socks5h", "https"), "https": proxy.replace("socks5h", "https")}, verify = False)
                content: str = response.content.decode()
                return content
            except Exception as error:
                log.failure("Encountered error while trying to check IP address: " + bold(str(error)) + ", site: " + bold(url), prefix = "Proxies")
                if url not in blacklist_:
                    blacklist_.append(url)
        sleep(5)

    return "n/a"
