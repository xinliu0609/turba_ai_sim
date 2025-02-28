import heapq
import math
import pytest
from gpu import GPU, Instruction
from simulation_engine import SimulationEngine, Event
from network import Network


def test_gpu_vars(gpu_instance: GPU) -> None:
    """Test that the GPU ID is correctly assigned."""
    assert gpu_instance.gpu_id == 0
    assert len(gpu_instance.compute_queue) == 3
    assert len(gpu_instance.comm_queue) == 1
    assert gpu_instance.compute_tflops == 200
    assert gpu_instance.chunk_size_bytes == 65536
    assert gpu_instance.network.object_id == 8


def test_gpu_parse_instruction(gpu_instance: GPU) -> None:
    """Test the parse instruction function, called by constructor,
    The instruction list is defined in conftest.py
    """
    assert len(gpu_instance.compute_queue) == 3

    compute_1: Instruction = gpu_instance.compute_queue.popleft()
    assert compute_1.ins_type == "COMPUTE"
    assert compute_1.source == "ALL"
    assert compute_1.destination == ""
    assert compute_1.size == 100000000
    assert compute_1.operation == "EXECUTE"

    compute_2: Instruction = gpu_instance.compute_queue.popleft()
    assert compute_2.ins_type == "COMPUTE"
    assert compute_2.source == "ALL"
    assert compute_2.destination == ""
    assert compute_2.size == 50000000
    assert compute_2.operation == "EXECUTE"

    compute_3: Instruction = gpu_instance.compute_queue.popleft()
    assert compute_3.ins_type == "COMPUTE"
    assert compute_3.source == "ALL"
    assert compute_3.destination == ""
    assert compute_3.size == 30000000
    assert compute_3.operation == "EXECUTE"

    assert len(gpu_instance.comm_queue) == 1

    comm_1: Instruction = gpu_instance.comm_queue.popleft()
    assert comm_1.ins_type == "COMMUNICATION"
    assert comm_1.source == "ALL"
    assert comm_1.destination == ""
    assert comm_1.size == 1048576
    assert comm_1.operation == "ALL_REDUCE"


def test_run_next_compute_and_done(gpu_instance: GPU) -> None:
    """Test the compute event generation"""
    engine_instance: SimulationEngine = gpu_instance.engine
    # register the gpu to the simulation engine
    engine_instance.register_object(0, gpu_instance)
    engine_instance.current_time_ns = 2500  # change the current time

    # extract info from the first compute event before calling the function
    compute_1: Instruction = gpu_instance.compute_queue[0]
    assert compute_1.size == 100000000
    assert gpu_instance.compute_tflops == 200
    # manually calculate the computing time
    compute_dur_ns: int = math.ceil((100000000 / (200 * 1e12)) * 1e9)

    # now call the function, we should expect an event created in the event queue
    assert len(engine_instance.event_queue) == 0
    gpu_instance.run_next_compute()
    assert len(gpu_instance.compute_queue) == 2  # the instruction is poped out
    assert len(engine_instance.event_queue) == 1  # new event in the queue
    event: Event = engine_instance.event_queue[0]
    assert event.timestamp == 2500 + compute_dur_ns
    assert event.event_type == "COMPUTE_DONE"
    assert event.target_id == 0
    assert event.args["ins"] == compute_1
    assert compute_1.start_time_ns == 2500  # the start time is assigned by the function

    # now, let's assume the time proceeded and GPU handles the event
    assert not gpu_instance.finished_instructions
    e: Event = heapq.heappop(engine_instance.event_queue)
    assert e == event
    assert len(engine_instance.event_queue) == 0
    gpu_instance.compute_done(event)
    assert len(gpu_instance.finished_instructions) == 1
    ins: Instruction = gpu_instance.finished_instructions[0]
    assert ins == compute_1  # make sure it's the same Instruction
    assert ins.end_time_ns == 2500 + compute_dur_ns
    # also the next instruction is poped and processed
    assert len(gpu_instance.compute_queue) == 1
    assert len(engine_instance.event_queue) == 1


def test_run_next_comm_and_done(gpu_instance: GPU) -> None:
    """Test the comm event generation"""
    engine_instance: SimulationEngine = gpu_instance.engine
    # register the gpu to the simulation engine
    engine_instance.register_object(0, gpu_instance)
    engine_instance.current_time_ns = 2500  # change the current time

    # extract info from the first compute event before calling the function
    assert len(gpu_instance.comm_queue) == 1
    comm_1: Instruction = gpu_instance.comm_queue[0]
    assert comm_1.size == 1048576

    # calling the function
    gpu_instance.run_next_comm()
    assert not gpu_instance.comm_queue
    assert len(engine_instance.event_queue) == 1  # new event in the queue
    event: Event = engine_instance.event_queue[0]
    assert event.timestamp == 2500
    assert event.event_type == "COMM_START"
    assert event.target_id == 8  # network object's ID
    assert event.args["size_bytes"] == comm_1.size
    assert event.args["src_gpu"] == 0
    assert event.args["ins"] == comm_1

    # now, assume 50000 ns later, communication finished
    # manually construct a "comm finish" event instead of network doing it
    engine_instance.current_time_ns = event.timestamp + 50000
    comm_finish_event: Event = Event(
        timestamp=event.timestamp + 50000,
        event_type="COMM_DONE",
        target_id=0,
        args={"ins": comm_1},
    )
    assert not gpu_instance.finished_instructions
    gpu_instance.communication_done(comm_finish_event)
    assert len(gpu_instance.finished_instructions) == 1
    ins: Instruction = gpu_instance.finished_instructions[0]
    assert ins == comm_1
    assert ins.start_time_ns == 2500
    assert ins.end_time_ns == comm_finish_event.timestamp
