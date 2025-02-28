import heapq

class Event:
    def __init__(self, timestamp, event_type, target_id, args):
        self.timestamp = timestamp
        self.event_type = event_type  # Example: "COMPUTE_DONE", "COMM_START"
        self.target_id = target_id    # The object ID that should handle this event
        self.args = args            # Additional arguments in dict format

    def __lt__(self, other):
        return self.timestamp < other.timestamp  # Priority queue ordering


class SimulationEngine:
    def __init__(self):
        self.event_queue = []
        self.objects = {}  # Maps object IDs (e.g., GPUs, Network) to objects
        self.current_time = 0

    def register_object(self, obj_id, obj):
        """Registers an object in the system by its ID."""
        self.objects[obj_id] = obj

    def schedule_event(self, event):
        """Adds an event to the priority queue."""
        heapq.heappush(self.event_queue, event)

    def dispatch_event(self, event):
        """Finds the correct object and lets it handle the event."""
        if event.target_id in self.objects:
            self.objects[event.target_id].handle_event(event)
        else:
            raise ValueError(f"No object found for ID: {event.target_id}")

    def run(self):
        """Processes all scheduled events until completion."""
        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            self.current_time = event.timestamp
            self.dispatch_event(event)

        print("Simulation completed.")
