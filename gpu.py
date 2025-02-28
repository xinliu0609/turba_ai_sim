from typing import List, Deque
from simulation_engine import Event, SimulationEngine
from network import Network
from collections import deque
import math


class Instruction:
    def __init__(
        self,
        event_type: str,
        source: str,
        destination: str,
        size: int,
        operation: str,
    ) -> None:
        self.ins_type: str = event_type  # rename it ins_type to avoid confusion of simulation event's type
        self.source: str = source
        self.destination: str = destination
        self.size: int = size  # for compute it's FLOPS, for comm it's Bytes
        self.operation: str = operation
        self.start_time_ns: int = 0
        self.end_time_ns: int = 0

    def __str__(self) -> str:
        s = "<Ins_type: " + self.ins_type
        s += ", Source: " + self.source
        s += ", Destination: " + self.destination
        s += ", Size: " + str(self.size)
        s += ", Operation: " + self.operation + ">"
        return s


class GPU:
    def __init__(
        self,
        gpu_id: int,
        instructions: List[str],
        compute_tflops: int,
        chunk_size_bytes: int,
        network: Network,
        engine: SimulationEngine,
    ):
        self.gpu_id: int = gpu_id
        self.compute_tflops: int = compute_tflops
        self.chunk_size_bytes: int = chunk_size_bytes
        self.network: Network = network
        self.engine: SimulationEngine = engine
        # separate compute and communication events into different queues
        # since they can run in parallel
        self.compute_queue: Deque[Instruction] = deque()
        self.comm_queue: Deque[Instruction] = deque()
        for instruction in instructions:
            ins: Instruction = self.parse_instruction(instruction)
            if ins.ins_type.lower() == "compute":
                self.compute_queue.append(ins)
            elif ins.ins_type.lower() == "communication":
                self.comm_queue.append(ins)
            else:
                raise ValueError(f"Unknown event type {ins.ins_type}")
        # store the finished instructions, output as results
        self.finished_instructions: List[Instruction] = []

    def parse_instruction(self, ins: str) -> Instruction:
        """Convert the instruction text to object."""
        ins_list: List[str] = [
            s.replace(" ", "") if s.strip() else "" for s in ins.split(",")
        ]
        if len(ins_list) != 5:
            raise AssertionError(f"Wrong trace format at {ins_list}")
        return Instruction(
            ins_list[0], ins_list[1], ins_list[2], int(ins_list[3]), ins_list[4]
        )

    def handle_event(self, event: Event) -> None:
        """Decides how to handle an event based on its type."""
        if event.event_type == "COMPUTE_DONE":
            self.compute_done(event)
        elif event.event_type == "COMM_DONE":
            self.communication_done(event)
        else:
            raise ValueError(
                f"Unknown event type {event.event_type} for GPU {self.gpu_id}"
            )

    def start_gpu(self) -> None:
        """Start executing both compute and comm instructions"""
        self.run_next_compute()
        self.run_next_comm()

    def run_next_compute(self) -> None:
        """Processes the next compute instruction in the queue."""
        if not self.compute_queue:
            return

        ins: Instruction = self.compute_queue.popleft()
        ins.start_time_ns = self.engine.current_time_ns
        tflops: int = ins.size
        compute_dur_ns: int = math.ceil((tflops / self.compute_tflops) * 1e-3)
        compute_done_event: Event = Event(
            timestamp=self.engine.current_time_ns + compute_dur_ns,
            event_type="COMPUTE_DONE",
            target_id=self.gpu_id,
            args={"ins": ins},
        )
        print(f"GPU {self.gpu_id} started computing at {self.engine.current_time_ns}")
        self.engine.schedule_event(compute_done_event)

    def compute_done(self, event: Event) -> None:
        """Handles computation completion and starts the next instruction."""
        print(f"GPU {self.gpu_id} finished computing at {event.timestamp}")

        # retrieve the instruction, log finished time and store it
        finished_ins: Instruction = event.args["ins"]
        finished_ins.end_time_ns = event.timestamp
        self.finished_instructions.append(finished_ins)
        self.run_next_compute()

    def run_next_comm(self) -> None:
        """Processes the next communication instruction in the queue.
        There will be an event COMM_START that handled by the network object
        """
        if not self.comm_queue:
            return

        ins: Instruction = self.comm_queue.popleft()
        ins.start_time_ns = self.engine.current_time_ns
        comm_start_event: Event = Event(
            timestamp=self.engine.current_time_ns,
            event_type="COMM_START",
            target_id=self.network.object_id,
            args={"size_bytes": ins.size, "src_gpu": self.gpu_id, "ins": ins},
        )
        self.engine.schedule_event(comm_start_event)

    def communication_done(self, event: Event) -> None:
        """Handles communication completion and starts the next instruction.
        This event is scheduled by the network object, after ALL of the transmission
        by this GPU is finished (all of the data to all of its destinations)
        """

        print(f"GPU {self.gpu_id} finished comm at {event.timestamp}")
        finished_ins: Instruction = event.args["ins"]
        finished_ins.end_time_ns = event.timestamp
        self.finished_instructions.append(finished_ins)
        self.run_next_comm()
