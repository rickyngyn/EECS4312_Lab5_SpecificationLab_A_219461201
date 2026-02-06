## Student Name: Ricky Nguyen
## Student ID: 219461201

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
from solution import suggest_slots

def test_single_event_blocks_overlapping_slots():
    """
    Functional requirement:
    Slots overlapping an event must not be suggested.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:15" in slots

def test_event_outside_working_hours_is_ignored():
    """
    Constraint:
    Events completely outside working hours should not affect availability.
    """
    events = [{"start": "07:00", "end": "08:00"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "09:00" in slots
    assert "16:00" in slots

def test_unsorted_events_are_handled():
    """
    Constraint:
    Event order should not affect correctness.
    """
    events = [
        {"start": "13:00", "end": "14:00"},
        {"start": "09:30", "end": "10:00"},
        {"start": "11:00", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert  slots[1] == "10:15"
    assert "09:30" not in slots

def test_lunch_break_blocks_all_slots_during_lunch():
    """
    Constraint:
    No meeting may start during the lunch break (12:00–13:00).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "12:00" not in slots
    assert "12:15" not in slots
    assert "12:30" not in slots
    assert "12:45" not in slots

"""TODO: Add at least 5 additional test cases to test your implementation."""

def test_event_touching_work_start():
    """
    Constraint:
    An event that ends exactly at the start of working hours should not block any slots.
    """
    events = [{"start": "08:00", "end": "09:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" in slots
    assert "09:15" in slots

def test_event_touching_work_end():
    """
    Constraint:
    An event that starts exactly at the end of working hours should not block any slots.
    """
    events = [{"start": "17:00", "end": "18:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "16:30" in slots
    assert "16:45" in slots

def test_event_touching_work_end():
    """
    Constraint:
    Meetings must fit fully within working hours.
    16:45 with a 30 min meeting would end after 17:00, so it must NOT be suggested.
    """
    events = [{"start": "17:00", "end": "18:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "16:30" in slots      # ends at 17:00
    assert "16:45" not in slots  # would end at 17:15


def test_overlapping_events_are_merged_effectively():
    """
    Constraint:
    Overlapping events behave like one continuous blocked interval.
    Also, a meeting cannot start exactly when a blocked interval ends (13:00),
    so 13:15 is the earliest valid start after lunch.
    """
    events = [
        {"start": "10:00", "end": "11:00"},
        {"start": "10:30", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "11:15" not in slots
    assert "12:00" not in slots
    assert "13:00" not in slots
    assert "13:15" in slots

def test_gap_smaller_than_meeting_duration_is_not_suggested():
    """
    Constraint:
    Free gaps shorter than the meeting duration must not produce any slots.
    """
    events = [
        {"start": "09:30", "end": "10:00"},
        {"start": "10:30", "end": "11:00"},
    ]
    # Gap from 10:00 to 10:30 is only 30 minutes.
    # Meeting duration is 45 minutes, so no slot should fit.
    slots = suggest_slots(events, meeting_duration=45, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:15" not in slots
    assert "09:00" in slots   # still valid before first event
