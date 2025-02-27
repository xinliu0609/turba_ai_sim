from simulation_engine import Event

class Network:
    def __init__(self, network_id, bandwidth, engine, gpus):
        self.network_id = network_id
        self.bandwidth = bandwidth  # Assume constant for now (no bandwidth sharing)
        self.engine = engine
        self.gpus = gpus  # Dictionary of GPU objects

    def handle_event(self, event):
        """Processes network-related events."""
        if event.event_type == "COMM_START":
            self.handle_comm_start(event)
        else:
            raise ValueError(f"Unknown event type {event.event_type} for Network")

    def handle_comm_start(self, event):
        """Handles the start of a communication event."""
        src_gpu, dst_gpu, data_size = event.args
        transfer_time = data_size / self.bandwidth
        completion_time = event.timestamp + transfer_time

        print(f"Network: GPU {src_gpu} starts sending {data_size} data to GPU {dst_gpu} at {event.timestamp}, will complete at {completion_time}")

        # Schedule the end of transmission event for the destination GPU
        self.engine.schedule_event(Event(
            completion_time, "COMM_END", dst_gpu, src_gpu
        ))
