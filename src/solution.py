## Student Name: Ricky Nguyen
## Student ID: 219461201

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
import datetime
from typing import List, Dict, Tuple

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    """
    Suggest possible meeting start times for a given day.

    Args:
        events: List of dicts with keys {"start": "HH:MM", "end": "HH:MM"}
        meeting_duration: Desired meeting length in minutes
        day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

    Returns:
        List of valid start times as "HH:MM" sorted ascending
    """
    # TODO: Implement this function
    def hhmm_to_minutes(t: str) -> int:
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    def minutes_to_hhmm(x: int) -> str:
        return f"{x // 60:02d}:{x % 60:02d}"

    WORK_START = hhmm_to_minutes("09:00")
    WORK_END = hhmm_to_minutes("17:00")
    LUNCH = (hhmm_to_minutes("12:00"), hhmm_to_minutes("13:00"))
    STEP = 15

    FRIDAY_CUTOFF = hhmm_to_minutes("15:00")
    def is_friday(d: str) -> bool:
        try:
            return datetime.date.fromisoformat(d).weekday() == 4
        except Exception:
            return False

    friday = is_friday(day)

    # Collect busy intervals (always include lunch)
    busy: List[Tuple[int, int]] = [LUNCH]

    for e in events:
        s = hhmm_to_minutes(e["start"])
        en = hhmm_to_minutes(e["end"])

        if en <= s:
            continue

        # Ignore events completely outside working hours
        if en <= WORK_START or s >= WORK_END:
            continue

        # Clip to working hours
        s = max(s, WORK_START)
        en = min(en, WORK_END)

        if en > s:
            busy.append((s, en))

    busy.sort(key=lambda x: x[0])

    # Merge overlapping intervals (touching is NOT merged)
    merged: List[Tuple[int, int]] = []
    for s, en in busy:
        if not merged:
            merged.append((s, en))
        else:
            last_s, last_en = merged[-1]
            if s < last_en:
                merged[-1] = (last_s, max(last_en, en))
            else:
                merged.append((s, en))

    def start_in_busy(t: int) -> bool:
        for bs, be in merged:
            if bs <= t < be:
                return True
        return False

    def start_at_busy_end(t: int) -> bool:
        for _, be in merged:
            if t == be:
                return True
        return False

    def overlaps_busy(start: int, end: int) -> bool:
        for bs, be in merged:
            if not (end <= bs or start >= be):
                return True
        return False

    results: List[str] = []
    latest_start = WORK_END - meeting_duration

    t = WORK_START
    while t <= latest_start:
        if friday and t > FRIDAY_CUTOFF:
            break

        if start_in_busy(t) or start_at_busy_end(t):
            t += STEP
            continue

        if t == WORK_START:
            if not start_in_busy(t) and not start_at_busy_end(t):
                results.append(minutes_to_hhmm(t))
            t += STEP
            continue

        # General rules
        if start_in_busy(t) or start_at_busy_end(t):
            t += STEP
            continue

        end_t = t + meeting_duration
        if end_t <= WORK_END and not overlaps_busy(t, end_t):
            results.append(minutes_to_hhmm(t))

        t += STEP

    return results