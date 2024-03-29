from __future__ import annotations

import sched
import time
from dataclasses import dataclass
from datetime import datetime
from datetime import time as dttime
from datetime import timedelta
from typing import Any

from .message import Message
from .theme import Personalization, Theme, parse_themes
from .utils import _str_to_time


def parse_schedule(
    sched_list: list[dict],
    theme_dict: dict[str, Theme],
) -> dict[dttime, Theme]:
    sched_dict: dict[dttime, ScheduleItem] = {}
    for sc in sched_list:
        sched_dict[_str_to_time(sc["time"])] = ScheduleItem(
            theme=theme_dict[sc["theme"]],
            confirm=sc["confirm"],
        )
    return sched_dict


@dataclass
class ScheduleItem:
    theme: Theme
    confirm: bool


class ThemeScheduler:
    def __init__(self, sched_dict: dict[dttime, ScheduleItem]) -> None:
        self._times = list(sched_dict.keys())
        self._items = list(sched_dict.values())
        self._sched_max = len(sched_dict)

    def current_scheduled_theme(self) -> ScheduleItem:
        i = -1
        cur_dt = datetime.now()
        cur_date = cur_dt.date()
        for t in self._times:
            if cur_dt < datetime.combine(cur_date, t):
                break
            i += 1
        return self._items[i]

    def next_scheduled_datetime(self) -> datetime:
        i = 0
        cur_dt = datetime.now()
        cur_date = cur_dt.date()
        for t in self._times:
            if cur_dt < datetime.combine(cur_date, t):
                break
            i += 1

        if i == self._sched_max:
            tmr_date = cur_date + timedelta(days=1)
            return datetime.combine(tmr_date, self._times[0])
        return datetime.combine(cur_date, self._times[i])


def run_scheduling(config: dict[str, list[dict] | Any]) -> None:
    message = Message()
    personalization = Personalization()

    application_delay = config.get("application_delay", 3.0)
    ask_interval_mins = config.get("ask_interval_mins", 30)

    try:
        theme_dict = parse_themes(theme_list=config["themes"])
        sched_dict = parse_schedule(
            sched_list=config["schedule"],
            theme_dict=theme_dict,
        )
    except KeyError as e:
        message.show_error(e)
        return
    theme_schedule = ThemeScheduler(sched_dict=sched_dict)

    def apply_scheduled_theme() -> None:
        time.sleep(application_delay)
        sched_item = theme_schedule.current_scheduled_theme()

        if sched_item.confirm:
            if not message.ask_ifyes(f"Change theme now?"):
                ask_dt = datetime.now() + timedelta(minutes=ask_interval_mins)
                next_dt = theme_schedule.next_scheduled_datetime()
                if ask_dt < next_dt:
                    sched_dt = ask_dt
                else:
                    sched_dt = next_dt
                schedule_theme_application(at_dt=sched_dt)
                return

        sched_item = theme_schedule.current_scheduled_theme()
        if sched_item.theme.mode is not None:
            personalization.apply_colormode(mode=sched_item.theme.mode)
        if sched_item.theme.wp is not None:
            personalization.apply_wallpaper(wp=sched_item.theme.wp)
        next_dt = theme_schedule.next_scheduled_datetime()
        schedule_theme_application(at_dt=next_dt)

    def schedule_theme_application(at_dt: datetime) -> None:
        scheduler = sched.scheduler()
        cur_now = datetime.now()
        scheduler.enter(
            delay=max((at_dt - cur_now).seconds, 1),
            priority=1,
            action=apply_scheduled_theme,
        )
        scheduler.run()

    apply_scheduled_theme()
