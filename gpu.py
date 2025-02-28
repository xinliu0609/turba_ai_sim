from simulation_engine import Event

class Instruction:
    def __init__(self, event_type, source, destination, size, operation):
        self.event_type = event_type
        self.source = source
        self.destination = destination
        self.size = size
        self.operation = operation
    
    def __str__(self):
        s = "<Event_type: " + self.event_type
        s += ", Source: " + self.source
        s += ", Destination: " + self.destination
        s += ", Size: " + str(self.size)
        s += ", Operation: " + self.operation + ">"
        return s

class GPU:
    def __init__(self, gpu_id, instructions, network, engine):
        self.gpu_id = gpu_id
        self.instructions = [self.parse_instruction(ins) for ins in instructions]
        self.network = network
        self.engine = engine
        self.current_instruction = 0  # Track execution progress

    def parse_instruction(self, ins):
        ins_list = [s.replace(" ", "") if s.strip() else "" for s in ins.split(",")]
        if len(ins_list) != 5:
            raise AssertionError(f"Wrong trace format at {ins_list}")
        instruction = Instruction(ins_list[0], ins_list[1], ins_list[2], int(ins_list[3]), ins_list[4])
        return instruction

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

        if instr.event_type.lower() == "compute":
            compute_time = instr.size
            print(f"GPU {self.gpu_id} starts computing for {compute_time} units")
            self.engine.schedule_event(Event(
                self.engine.current_time + compute_time, "COMPUTE_DONE", self.gpu_id
            ))

        elif instr.event_type.lower() == "communication":
            target_gpu, data_size = 0, instr.size
            print(f"GPU {self.gpu_id} prepares to send {data_size} data to GPU {target_gpu}")
            self.engine.schedule_event(Event(
                self.engine.current_time, "COMM_START", self.network.object_id, self.gpu_id, target_gpu, data_size
            ))

    def compute_done(self, event):
        """Handles computation completion and starts the next instruction."""
        print(f"GPU {self.gpu_id} finished computing at {event.timestamp}")
        self.start_next_instruction()

    def communication_done(self, event):
        """Handles communication completion and starts the next instruction."""
        print(f"GPU {self.gpu_id} received data from GPU {event.args[0]} at {event.timestamp}")
        self.start_next_instruction()