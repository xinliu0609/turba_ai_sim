from simulation_engine import Event
import math

class Network:
    def __init__(self, object_id, num_gpus, bandwidth_gbps, topology, engine):
        print(f"get object id = {object_id}")
        self.object_id = object_id
        self.num_gpus = num_gpus
        self.bandwidth_gbps = bandwidth_gbps  # Assume constant for now (no bandwidth sharing)
        self.topology = topology
        self.engine = engine

    def handle_event(self, event):
        """Processes network-related events."""
        if event.event_type == "COMM_START":
            self.handle_comm_start(event)
        else:
            raise ValueError(f"Unknown event type {event.event_type} for Network")

    def handle_comm_start(self, event):
        """Handles the start of a communication event."""
        src_gpu = event.args["src_gpu"]
        size_bytes = event.args["size_bytes"]
        transfer_time_ns = math.ceil(size_bytes * 8  / self.bandwidth_gbps)

        print(f"Network: GPU {src_gpu} starts sending {size_bytes} data to all other GPUs")

        # Schedule the end of transmission event for the destination GPU
        # Pass the instruction back to the source GPU
        comm_finish_event = Event(timestamp=event.timestamp + transfer_time_ns,
                                  event_type="COMM_DONE",
                                  target_id=src_gpu,
                                  args={"ins": event.args["ins"]})
        self.engine.schedule_event(comm_finish_event)
