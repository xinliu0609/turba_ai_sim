from simulation_engine import Event

class GPU:
    def __init__(self, gpu_id, instructions, network, engine):
        self.gpu_id = gpu_id
        self.instructions = instructions  # List of (type, duration or target, data_size)
        self.network = network
        self.engine = engine
        self.current_instruction = 0  # Track execution progress

    def handle_event(self, event):
        """Decides how to handle an event based on its type."""
        if event.event_type == "COMPUTE_DONE":
            self.compute_done(event)
        elif event.event_type == "COMM_END":
            self.communication_done(event)
        else:
            raise ValueError(f"Unknown event type {event.event_type} for GPU {self.gpu_id}")

    def start_next_instruction(self):
        """Processes the next instruction in the list."""
        if self.current_instruction >= len(self.instructions):
            return  # All instructions completed

        instr = self.instructions[self.current_instruction]
        self.current_instruction += 1

        if instr[0] == "compute":
            compute_time = instr[1]
            print(f"GPU {self.gpu_id} starts computing for {compute_time} units")
            self.engine.schedule_event(Event(
                self.engine.current_time + compute_time, "COMPUTE_DONE", self.gpu_id
            ))

        elif instr[0] == "communicate":
            target_gpu, data_size = instr[1], instr[2]
            print(f"GPU {self.gpu_id} prepares to send {data_size} data to GPU {target_gpu}")
            self.engine.schedule_event(Event(
                self.engine.current_time, "COMM_START", self.network.network_id, self.gpu_id, target_gpu, data_size
            ))

    def compute_done(self, event):
        """Handles computation completion and starts the next instruction."""
        print(f"GPU {self.gpu_id} finished computing at {event.timestamp}")
        self.start_next_instruction()

    def communication_done(self, event):
        """Handles communication completion and starts the next instruction."""
        print(f"GPU {self.gpu_id} received data from GPU {event.args[0]} at {event.timestamp}")
        self.start_next_instruction()