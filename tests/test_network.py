import pytest
from network import Network
from simulation_engine import SimulationEngine, Event


def test_network_vars(network_instance: Network) -> None:
    """Test that the network has the correct variables."""
    assert network_instance.object_id == 8
    assert network_instance.num_gpus == 8
    assert network_instance.bandwidth_GBps == 25
    assert network_instance.topology == "ring"


"""
def test_communication_event(network_instance: Network) -> None:
    Test that a COMM_START event is scheduled correctly.
    event = Event(
        10, "COMM_START", "network", {"src_gpu": 0, "dst_gpu": 1, "data_size": 500}
    )
    network_instance.handle_event(event)

    assert len(network_instance.engine.event_queue) == 1
"""
