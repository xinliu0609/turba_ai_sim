import pytest
from simulation_engine import SimulationEngine, Event


@pytest.fixture
def sim_engine() -> SimulationEngine:
    """Fixture to create a fresh SimulationEngine instance before each test."""
    return SimulationEngine()


def test_event_queue_empty(sim_engine: SimulationEngine) -> None:
    """Test that the event queue starts empty."""
    assert len(sim_engine.event_queue) == 0


def test_event_scheduling(sim_engine: SimulationEngine) -> None:
    """Test that an event is scheduled correctly."""
    event: Event = Event(
        timestamp=10,
        event_type="TEST_EVENT",
        target_id=1,
        args={"test_key": "test_value"},
    )
    sim_engine.schedule_event(event)
    assert len(sim_engine.event_queue) == 1

    e = sim_engine.event_queue[0]
    e.timestamp = 10
    e.event_type = "TEST_EVENT"
    e.target_id = 1
    e.args["test_key"] = "test_value"


def test_event_execution_order(sim_engine: SimulationEngine) -> None:
    """Test that events execute in the correct timestamp order."""
    event1: Event = Event(20, "EVENT_1", 1, {})
    event2: Event = Event(10, "EVENT_2", 1, {})
    sim_engine.schedule_event(event1)
    sim_engine.schedule_event(event2)

    assert sim_engine.event_queue[0] == event2  # The earliest event should be first
