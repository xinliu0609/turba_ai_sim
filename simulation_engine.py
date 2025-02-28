from __future__ import annotations  # Enables forward references
import heapq
from typing import Any, Dict, List


class Event:
    def __init__(
        self, timestamp: int, event_type: str, target_id: int, args: Dict[str, Any]
    ) -> None:
        self.timestamp: int = timestamp
        self.event_type: str = event_type  # Example: "COMPUTE_DONE", "COMM_START"
        self.target_id: int = target_id  # The object ID that should handle this event
        self.args: Dict[str, Any] = args  # Additional arguments in dict format

    def __lt__(self, other: Event) -> bool:
        return self.timestamp < other.timestamp  # Priority queue ordering


class SimulationEngine:
    def __init__(self) -> None:
        self.event_queue: List[Event] = []
        self.objects: Dict[int, Any] = {}  # Maps object IDs to objects (GPU/Network)
        self.current_time_ns: int = 0

    def register_object(self, obj_id: int, obj: Any) -> None:
        """Registers an object in the system by its ID."""
        self.objects[obj_id] = obj

    def schedule_event(self, event: Event) -> None:
        """Adds an event to the priority queue."""
        heapq.heappush(self.event_queue, event)

    def dispatch_event(self, event: Event) -> None:
        """Finds the correct object and lets it handle the event."""
        if event.target_id in self.objects:
            self.objects[event.target_id].handle_event(event)
        else:
            raise ValueError(f"No object found for ID: {event.target_id}")

    def run(self) -> None:
        """Processes all scheduled events until completion."""
        while self.event_queue:
            event: Event = heapq.heappop(self.event_queue)
            self.current_time = event.timestamp
            self.dispatch_event(event)

        print("Simulation completed.")
