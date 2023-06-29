import time
from contextlib import ContextDecorator
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Callable
from typing import Optional


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


@dataclass
class Timer(ContextDecorator):
    """Time your code using a class, context manager, or decorator"""

    total: int = 0
    name: Optional[str] = 'Timer'
    text: str = "Elapsed time: {:0.4f} seconds"
    logger: Optional[Callable[[str], None]] = print
    _start_time: Optional[float] = field(default=None, init=False, repr=False)

    def start(self) -> None:
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        # Calculate elapsed time
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        # Report elapsed time
        if self.logger:
            self.logger(self.text.format(elapsed_time) + f" [{self.name}]")
        if self.name:
            #self.timers[self.name] += elapsed_time
            self.total += elapsed_time

        return elapsed_time

    def __enter__(self) -> "Timer":
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        """Stop the context manager timer"""
        self.stop()

    def __del__(self):
        # Данный метод вызывается несколько раз
        # Причем лишь один раз с текущими значениями полей
        # А в остальных с дефолтными

        # В конце выведем тотал
        if self.total > 0:
            self.logger(f"Total time for {self.name}: {self.total}")
