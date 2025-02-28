from simulation_engine import Event, SimulationEngine
import math


class Network:
    def __init__(
        self,
        object_id: int,
        num_gpus: int,
        bandwidth_GBps: int,
        topology: str,
        engine: SimulationEngine,
    ) -> None:
        print(f"get object id = {object_id}")
        self.object_id: int = object_id
        self.num_gpus: int = num_gpus
        self.bandwidth_GBps: int = bandwidth_GBps  # Assume GPUs have the same bandwidth
        self.topology: str = topology
        self.engine: SimulationEngine = engine

    def handle_event(self, event: Event) -> None:
        """Processes network-related events."""
        if event.event_type == "COMM_START":
            self.handle_comm_start(event)
        else:
            raise ValueError(f"Unknown event type {event.event_type} for Network")

    def handle_comm_start(self, event: Event) -> None:
        """Handles the start of a communication event."""
        src_gpu: int = event.args["src_gpu"]
        size_bytes: float = event.args["size_bytes"]
        transfer_time_ns: int = math.ceil((size_bytes / self.bandwidth_GBps))

        print(
            f"Network: GPU {src_gpu} starts sending {size_bytes} data to all other GPUs"
        )

        # Schedule the end of transmission event for the destination GPU
        # Pass the instruction back to the source GPU
        comm_finish_event: Event = Event(
            timestamp=event.timestamp + transfer_time_ns,
            event_type="COMM_DONE",
            target_id=src_gpu,
            args={"ins": event.args["ins"]},
        )
        self.engine.schedule_event(comm_finish_event)
