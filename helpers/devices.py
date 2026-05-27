from random              import choice
from dataclasses         import dataclass, field

try:
    from .utils          import directories
except ImportError:
    from helpers.utils   import directories

class data:
    languages:   list[str] = ["pl_PL", "en_US", "en_GB"]
    user_agents: list[str] = directories.user_agents.read_text(encoding = "UTF-8").splitlines()

@dataclass
class IPhone:
    name: str

    width:  int = field(init = False)
    height: int = field(init = False)

    device_scale_factor:  float = 3.00
    max_touch_points:     int = 5
    hardware_concurrency: int = 4

    touch:  bool = True
    mobile: bool = True

    user_agent: str = field(init = False)
    dark_mode:  bool = field(init = False)
    languages:  str = field(init = False)

    def __post_init__(self):
        self.user_agent = choice(data.user_agents)
        self.dark_mode  = choice([True, False])
        self.languages  = choice(data.languages)

@dataclass
class IPhoneSE(IPhone):
    def __post_init__(self) -> IPhone:
        super().__post_init__()
        self.name: str = "iPhone SE"

        self.width:  int = 375
        self.height: int = 667

        self.device_scale_factor: float = 2.00

        self.hardware_concurrency: int = 4

@dataclass
class IPhone11(IPhone):
    def __post_init__(self) -> IPhone:
        super().__post_init__()
        self.name: str = "iPhone 11"

        self.width:  int = 414
        self.height: int = 896

        self.device_scale_factor: float = 2.00

@dataclass
class IPhone15(IPhone):
    def __post_init__(self) -> IPhone:
        super().__post_init__()
        self.name: str = "iPhone 15"

        self.width:  int = 393
        self.height: int = 852

@dataclass
class IPhone14(IPhone):
    def __post_init__(self) -> IPhone:
        super().__post_init__()
        self.name: str = "iPhone 14"

        self.width, self.height = choice([
            (393, 852),
            (430, 932)
        ])

@dataclass
class IPhone13(IPhone):
    def __post_init__(self) -> IPhone:
        super().__post_init__()
        self.name: str = "iPhone 13"

        self.width, self.height = choice([
            (390, 844),
            (428, 926)
        ])

@dataclass
class IPhone12(IPhone):
    def __post_init__(self) -> IPhone:
        super().__post_init__()
        self.name: str = "iPhone 12"

        self.width, self.height = choice([
            (390, 844),
            (428, 926)
        ])
