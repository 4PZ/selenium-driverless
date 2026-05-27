import sys

from os                  import path
from re                  import compile
from re                  import search
from time                import time
from typing              import Any
from typing              import Self
from inspect             import stack
from datetime            import datetime
from pygments            import highlight
from traceback           import TracebackException
from pygments.lexers     import PythonTracebackLexer
from pygments.lexers     import get_lexer_by_name
from collections.abc     import Callable as Function
from pygments.formatters import TerminalFormatter
from pygments.formatters import get_formatter_by_name

sys.tracebacklimit = 10

def set_highlighted_exception_hook():
    lexer: PythonTracebackLexer = get_lexer_by_name("py3tb", stripall = True)
    formatter: TerminalFormatter = TerminalFormatter(style = "rrt")

    def exception_hook(exception_type: object, exception_value: object, exception_traceback: object) -> None:
        traceback_exception = TracebackException(exception_type, exception_value, exception_traceback, capture_locals=False)
        for frame in traceback_exception.stack:
            frame.filename: str = path.relpath(frame.filename)
        formatted: str = "".join(traceback_exception.format())
        if "KeyboardInterrupt" not in formatted:
            sys.stderr.write("\n" + highlight(formatted, lexer, formatter))

    sys.excepthook: object = exception_hook

def timestamp() -> int:
    return int(time())

def bold(content: str, end_color: str = "\033[0m") -> str:  return BOLD  + str(content) + end_color

def black(content: str, end_color: str = "\033[0m") -> str: return BLACK + str(content) + end_color

def white(content: str, end_color: str = "\033[0m") -> str: return WHITE + str(content) + end_color

def yellow(content: str, end_color: str = "\033[0m") -> str: return YELLOW + str(content) + end_color

def magenta(content: str, end_color: str = "\033[0m") -> str: return MAGENTA + str(content) + end_color

def purple(content: str, end_color: str = "\033[0m") -> str: return PURPLE + str(content) + end_color

def cyan(content: str, end_color: str = "\033[0m") -> str: return CYAN + str(content) + end_color

def meta(content: str, end_color: str = "\033[0m") -> str: return META + str(content) + end_color

META:      str = "\033[38;5;26m"
BOLD:      str = "\033[1m"
WHITE:     str = "\033[37m"
MAGENTA:   str = "\033[38;5;97m"
RED:       str = "\033[38;5;196m"
GREEN:     str = "\033[38;5;40m"
YELLOW:    str = "\033[38;5;220m"
CYAN:      str = "\033[38;5;50m"
BLUE:      str = "\033[38;5;21m"
PINK:      str = "\033[38;5;176m"
BLACK:     str = "\033[90m"
PURPLE:    str = "\033[38;5;105m"
ENDC:      str = "\033[0m"
BLINK:     str = "\033[5m"
EMPTY:     str = ""

class Logger:
    def __init__(self, prefix: str = "Browser", longest: int = 24, lm: int = 74):
        self.prefix_old: str = prefix
        self.longest:    int = longest
        self.lm:         int = lm

        self.get_prefix(prefix)

    def get_time(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def make_spaces(self, length: int) -> str:
        return "".join([" " for _ in range(length)])

    def make_space(self, amount: int = 0, content: str = None):
        if content:
            if len(content) > self.longest:
                self.longest = len(content)
                return ""

            return self.make_spaces(self.longest - len(content))

        return self.make_spaces(amount)

    def bracket(self, content: str, color: str = PINK) -> str:
        return color + BOLD + "[" + content + "]" + ENDC

    def prefix_to_color(self, prefix: str) -> str:
        if "Browser" in prefix: return META
        if "Program" in prefix: return BLACK

    def make_date(self) -> str:
        return bold("┃ " + self.bracket(self.get_time(), color = WHITE) + bold(" ┃"))

    def make_message_clean(self, message: str, color: str) -> str:
        message_clean: str = message.replace(ENDC, "").replace(BOLD, "").replace(color, "")
        if len(message_clean) > self.lm: self.lm = len(message_clean) + 2
        return message_clean

    def get_level(self, caller: str) -> str:
        match caller:
            case "info": return "Actions"
            case _:
                level: str = caller[0].upper() + caller[1:]
                if len(level) != 7:
                    level: str = "Actions"
                return level

    def make_call_function(self, call_function: str) -> str:
        if call_function != "<module>":
            return call_function + "()"
        else:
            return "__main__()"

    def level_to_color(self, level: str, prefix_local: str) -> str:
        match level:
            case "Failure": return RED
            case "Success": return GREEN
            case "Warning": return YELLOW
            case "Actions": return self.prefix_to_color(prefix_local)
            case _:         return GREEN

    def fix_message(self, message: str) -> str:
        if message.endswith("."):
            message: str = message[:-1]
        return message

    def make_arrow(self) -> str:
        return bold("─⪢")

    def replace_bold(self, content: str, color: str) -> str:
        return content.replace("\x1b[0m", color.replace("\\033", "\1xb"), -1)

    def make_prefix_local(self, level: str) -> str:
        return self.prefix

    def make_message(self, message: str, color: str) -> str:
        return "\x1b[0m" + self.replace_bold(self.bracket(color + message, color = color), color)

    def make_level(self, level: str, color: str, call_function: str) -> str:
        return self.bracket(color + level, color = color) + self.make_space(content = call_function) + color + call_function + ENDC

    def make_prefix(self: Self, prefix: str) -> str:
        return prefix + self.make_space()

    def message(self: Self, caller: str, message: str, start: int, end: int, new_line: bool, _: None, call_function: Any) -> str:
        if new_line: print(bold("          ┃            ┃"))

        message:       str = self.fix_message(message)
        call_function: str = self.make_call_function(call_function)
        level:         str = self.get_level(caller)
        prefix:        str = self.make_prefix_local(level)
        color:         str = self.level_to_color(level, prefix)

        print(" ".join(
            [
                self.make_prefix(prefix),
                self.make_date(),
                self.make_level(level, color, call_function),
                self.make_arrow(),
                self.make_message(message, color),
                self.make_timer(start, end, message, color),
                ENDC
            ]
        ))

    def format_timer(self: Self, end: int, start: int) -> str:
        return str(end - start)[:5] + "s"

    def make_timer(self: Self, start: int, end: int, message: str, color: str) -> str:
        message_clean: str = self.make_message_clean(message, color)
        if start:
            if not end:
                end: int = timestamp()
            return self.make_space(amount = (self.lm - len(message_clean)) - 1) + BLACK + "In " + self.make_arrow() + " " + BLACK + BLINK + bold(self.format_timer(end, start))
        return ""

    def get_prefix(self: Self, prefix: str) -> None:
        match prefix:
            case "Program": self.prefix: str = black("[", end_color = EMPTY) + bold(prefix) + black("]")
            case "Browser": self.prefix: str = meta("[", end_color = EMPTY) + bold(prefix) + meta("]")

    def __process__(self, message: str, start: int = None, end: int = None, new_line: bool = False, prefix: str = None):
        if prefix: self.get_prefix(prefix)
        else:      self.prefix: str = meta("[", end_color = EMPTY) + bold("Browser") + meta("]")

        values: list[Any] = list({**locals()}.values())

        function_from_call   = compile(r"\w+(?=\()")
        _, call_frame, *_    = stack()
        _, _, _, _, call, *_ = call_frame

        try:    caller = search(function_from_call, str(call)).group()
        except Exception: return values

        values[0] = caller
        values.append(call_frame.function)

        self.message(*values)

    info:    Function = __process__
    success: Function = __process__
    failure: Function = __process__
    warning: Function = __process__

set_highlighted_exception_hook()

log = Logger()
