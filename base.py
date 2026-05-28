import asyncio
from random                import choice
from warnings              import filterwarnings

filterwarnings("ignore")

from helpers.devices       import IPhone, IPhoneSE, IPhone11, IPhone12, IPhone13, IPhone14, IPhone15
from helpers.logger        import Logger, bold
from helpers.events        import set_idle_override, set_touch_points, set_cores, set_dark_mode, set_touch_mode, set_network_enable, set_mobile_metrics, set_user_agent_metadata, set_focus_emulation, set_geolocation, load_scripts, load_spoofing_script, set_canvas_fingerprint, set_fake_webrtc, set_blocked_urls, set_audio_fingerprint, load_stealth_script
from helpers.resources     import make_prefs, make_arguments, button_sleep, fields, buttons
from helpers.utils         import directories, scripts
from selenium_driverless   import webdriver

log: object = Logger(prefix = "Browser")

class Base:
    driver: object = None

    class config:
        debug:      bool = False
        trustscore: bool = True
        devtools:   bool = False
        cache:      bool = True
        profiles:   bool = True
        proxy:      str = ""

        binary_location: str = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        cache_directory: str = str(directories.cache)
        profile_directory: str = str(directories.profile)

        start_url: str = "https://example.org"

        blocked_urls: list[str] = [
            # Proof of concept: block a specific request url on every new session.
            "https://example.org/tracker.js",
        ]

        scripts:   list[str] = [
            scripts.utils,
            scripts.gpu,
        ]

    def __init__(self):
        self.pick_device()

    def pick_device(self):
        available_devices = [
            IPhoneSE(IPhone),
            IPhone11(IPhone),
            IPhone12(IPhone),
            IPhone13(IPhone),
            IPhone14(IPhone),
            IPhone15(IPhone)
        ]

        self.device: object = choice(available_devices)

        log.info("Picked device (" + bold(self.device.name) + ")")

    def make_options(self) -> webdriver.ChromeOptions:
        options: webdriver.ChromeOptions = webdriver.ChromeOptions()

        options.binary_location = self.config.binary_location

        for pref, value in make_prefs(self.device).items():
            options.update_pref(pref, value)

        for argument in make_arguments(self.device, self.config):
            options.add_argument(argument)

        if self.config.devtools:
            options.add_argument("--auto-open-devtools-for-tabs")

        return options

    async def initialize_driver(self, driver: webdriver.Chrome):
        log.info("Initializing driver")
        self.driver = driver

        directories.cache.mkdir(parents = True, exist_ok = True)
        directories.profile.mkdir(parents = True, exist_ok = True)

        for function in [
            set_fake_webrtc,
            set_network_enable,
            set_focus_emulation,
            load_stealth_script,
            set_audio_fingerprint,
            set_canvas_fingerprint,
        ]:
            function(driver)

        for function in [
            set_idle_override,
            set_touch_points,
            set_cores,
            set_dark_mode,
            set_touch_mode,
            load_spoofing_script,
            set_mobile_metrics,
            set_user_agent_metadata,
        ]:
            function(driver, self.device)

        if self.config.blocked_urls:
            set_blocked_urls(driver, self.config.blocked_urls)
            log.info(f"Blocked {bold(len(self.config.blocked_urls))} URL pattern(s)")

        if self.config.scripts:
            load_scripts(driver, self.config.scripts, edit = False)
            log.info(f"Loaded {bold(len(self.config.scripts))} JavaScript file(s)")

        if self.config.proxy:
            set_geolocation(
                driver,
                {
                    "http": self.config.proxy,
                    "https": self.config.proxy
                }
            )

        if self.config.trustscore:
            log.info("Navigating to trust score check sites...")
            await driver.get("https://abrahamjuliot.github.io/creepjs/", wait_load=True)
            await asyncio.sleep(300000)

        log.success("Initialized driver")

    async def start(self):
        options = self.make_options()

        self.driver = await webdriver.Chrome(options = options).__aenter__()
        await self.initialize_driver(self.driver)

        return self.driver

    async def stop(self):
        if self.driver:
            await self.driver.quit()
            self.driver = None
            log.info("Closed driver")

    async def visit(self, url: str = None):
        if not self.driver:
            raise RuntimeError("Driver is not initialized")

        destination: str = url or self.config.start_url

        log.info(f"Navigating to {bold(destination)}")
        await self.driver.get(destination, wait_load = True)
        await asyncio.sleep(button_sleep.general)

        current_url = await self.driver.current_url
        log.success(f"Loaded {bold(current_url)}")

        return current_url

    async def element_click(self, by: str, value: str, name: str = None) -> bool:
        await asyncio.sleep(button_sleep.clicked)

        try:
            element = await self.driver.find_element(by, value, timeout = 5)
            await element.click()
            log.info(f"Clicked {bold(name or value)}")
            return True
        except Exception as error:
            log.warning(f"Error when trying to click {bold(name or value)}: {error}")
            return False

    async def element_write(self, by: str, value: str, keys: str, click_on: bool = False, name: str = None) -> bool:
        await asyncio.sleep(button_sleep.typing)

        try:
            element = await self.driver.find_element(by, value, timeout = 5)
            await element.send_keys(keys, click_on = click_on)
            log.info(f"Typed into {bold(name or value)}")
            return True
        except Exception as error:
            log.warning(f"Error when trying to type into {bold(name or value)}: {error}")
            return False

async def main():
    session: object = Base()

    try:
        await session.start()
        await session.visit()

        await session.element_write(
            *fields.example_input,
            keys = "placeholder text",
            click_on = True,
            name = "example input"
        )
        
        await session.element_click(
            *buttons.example_button,
            name = "example button"
        )

        if session.config.debug:
            await asyncio.sleep(300000)
    finally:
        await session.stop()

if __name__ == "__main__":
    asyncio.run(main())
