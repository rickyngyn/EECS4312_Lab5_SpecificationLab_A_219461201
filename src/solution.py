## Student Name: Ricky Nguyen
## Student ID: 219461201

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
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
    WORK_END   = hhmm_to_minutes("17:00")
    LUNCH      = (hhmm_to_minutes("12:00"), hhmm_to_minutes("13:00"))
    STEP = 15

    # Collect busy intervals
    busy: List[Tuple[int, int]] = [LUNCH]

    for e in events:
        s = hhmm_to_minutes(e["start"])
        e_ = hhmm_to_minutes(e["end"])
        if e_ <= s:
            continue

        # Ignore events fully outside working hours
        if e_ <= WORK_START or s >= WORK_END:
            continue

        # Clip to working hours
        s = max(s, WORK_START)
        e_ = min(e_, WORK_END)
        busy.append((s, e_))

    # Sort by start time
    busy.sort(key=lambda x: x[0])

    # Merge only true overlaps (touching is NOT merged)
    merged: List[Tuple[int, int]] = []
    for s, e in busy:
        if not merged:
            merged.append((s, e))
        else:
            last_s, last_e = merged[-1]
            if s < last_e:  # overlap only
                merged[-1] = (last_s, max(last_e, e))
            else:
                merged.append((s, e))

    # Asymmetric conflict rule from tests
    def conflicts(cs: int, ce: int) -> bool:
        for bs, be in merged:
            # Block if start touches or overlaps end
            if cs <= be and ce > bs:
                return True
        return False

    results: List[str] = []
    latest_start = WORK_END - meeting_duration

    t = WORK_START
    while t <= latest_start:
        if not conflicts(t, t + meeting_duration):
            results.append(minutes_to_hhmm(t))
        t += STEP

    return results
