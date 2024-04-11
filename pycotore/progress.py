import sys
import os
from datetime import datetime
from logging import getLogger

# basicConfig(level=DEBUG)
_logger = getLogger(__name__)


class ProgressBar():
    """
    Progress bar class
    """

    show_suffix: bool = True
    show_preffix: bool = True
    show_bar: bool = True

    def __init__(
                self,
                base_marker: str = ".",
                done_marke: str = "#",
                current_marker: str = ">",
                show_percents: bool = True,
                show_estimate: bool = True,
                show_runtime: bool = True
            ):
        self.preffix: str = ""
        self.suffix: str = ""
        self.bar_length: int = 0
        self.bar_size: int = 0
        self.terminal_size: int = os.get_terminal_size().columns
        self.progress: float = 0.00
        self.total: float = 100.00
        self.done_marker: str = done_marke
        self.in_progress_marker: str = base_marker
        self.current_marker: str = current_marker
        self.percents: float = "000.00%"
        self.show_percents: bool = show_percents
        self.show_numbers: bool = False
        self.time_start = datetime.now()
        self.show_estimate: bool = show_estimate
        self.estimate = "|ETA: 00:00:00"
        self.run_time = "|RUN: 00:00:00"
        self.show_runtime: bool = show_runtime

    def flush_line(self) -> None:
        sys.stdout.write("\n")
        sys.stdout.flush()

    def __update_terminal_size(self) -> None:
        self.terminal_size = os.get_terminal_size().columns
        self.__update_bar_length()

    def __update_run_time(self) -> None:
        now = datetime.now()
        run_time = now - self.time_start
        self.run_time = f"|RUN: {run_time.seconds // 3600:0>2}:{run_time.seconds // 60:0>2}:{run_time.seconds % 60:0>2}"

    def __calculate_estimate(self) -> None:
        now = datetime.now()
        run_time = now - self.time_start
        run_data_left = self.total - self.progress
        run_avg_speed = int(self.progress // run_time.total_seconds())
        run_estimate = int(run_data_left // run_avg_speed)
        self.estimate = f"|ETA: {run_estimate // 3600:0>2}:{run_estimate // 60:0>2}:{run_estimate % 60:0>2}"

    def __update_percent_done(self) -> None:
        percents = round(self.progress * 100 / self.total, 2)
        self.percents = f"{percents:0>6.2f}%"

    def __update_bar_length(self) -> None:
        """
        Updating progress bar total size
        """
        self.bar_length = len(self.preffix) + len(self.suffix)
        self.bar_size = self.terminal_size - self.bar_length - 3
        if self.show_percents:
            self.bar_size -= len(self.percents)
        if self.show_estimate:
            self.bar_size -= len(self.estimate)
        if self.show_runtime:
            self.bar_size -= len(self.run_time)

    def __format_bar(self) -> str:
        bar = []
        finished = int(self.bar_size * self.progress / self.total)
        finished_mark = self.done_marker * finished
        in_progress_mark = self.in_progress_marker * (self.bar_size - finished - 1)
        if self.bar_size <= finished:
            self.current_marker = ""
        if self.preffix:
            bar.append(f"{self.preffix} ")
        if self.show_bar:
            bar.append(f"[{finished_mark}{self.current_marker}{in_progress_mark}]")
        if self.show_percents:
            bar.append(self.percents)
        if self.show_estimate:
            bar.append(self.estimate)
        if self.show_runtime:
            bar.append(self.run_time)
        if self.show_suffix:
            bar.append(f"|{self.suffix}")
        bar.append("\r")
        return "".join(bar)

    def draw(self) -> None:
        """
        Draw a progress bar
        """
        if self.show_percents:
            self.__update_percent_done()
        if self.show_estimate:
            self.__calculate_estimate()
        if self.show_runtime:
            self.__update_run_time()
        self.__update_terminal_size()
        bar = self.__format_bar()
        sys.stdout.write(bar)
        sys.stdout.flush()

    def set_prefix(self, preffix: str) -> None:
        """
        Change bar prefix
        """
        self.preffix = preffix
        self.__update_bar_length()

    def set_suffix(self, suffix: str) -> None:
        """
        Change bar suffix
        """
        self.suffix = suffix
        self.__update_bar_length()

    def set_bar_size(self, size: int) -> None:
        """
        Change bar size
        """
        try:
            if int(size):
                self.bar_size = size
        except ValueError:
            _logger.warning("Unable to set bar size")

    def update_progress(self, done: float) -> None:
        """
        Update progress done percentage
        """
        self.progress = done

    def set_total(self, total) -> None:
        """
        Set progress bar total value
        """
        try:
            if float(total):
                self.total = total
        except ValueError:
            _logger.warning("Unable to set total")

    def __clear_line(self, line) -> None:
        sys.stdout.write("\033[K")
        sys.stdout.flush()
