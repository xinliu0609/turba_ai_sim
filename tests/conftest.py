import pytest
from simulation_engine import SimulationEngine
from network import Network
from gpu import GPU
from typing import Optional, Dict, Any


@pytest.fixture
def sim_engine_instance() -> SimulationEngine:
    """Provides a fresh SimulationEngine instance for all tests."""
    return SimulationEngine()


@pytest.fixture
def network_instance(
    sim_engine_instance: SimulationEngine,
    request: Optional[pytest.FixtureRequest] = None,
) -> Network:
    """
    Provides a Network instance with configurable parameters.
    Default params are defined below.

    Use @pytest.mark.parametrize("network", [{"bandwidth": X}], indirect=True) to override.
    """
    network_params: Dict[str, Any] = getattr(
        request,
        "param",
        {
            "object_id": 8,
            "num_gpus": 8,
            "bandwidth_GBps": 25,
            "topology": "ring",
        },
    )
    return Network(
        network_params["object_id"],
        network_params["num_gpus"],
        network_params["bandwidth_GBps"],
        network_params["topology"],
        sim_engine_instance,
    )


@pytest.fixture
def gpu_instance(
    sim_engine_instance: SimulationEngine,
    network_instance: Network,
    request: Optional[pytest.FixtureRequest] = None,
) -> GPU:
    """
    Provides a GPU instance with configurable parameters.
    Default params are defined below.

    Use @pytest.mark.parametrize("gpu_instance", [{"gpu_id": X, "instructions": [...] }], indirect=True)
    """

    instruction_list = [
        "COMPUTE, ALL, , 100000000, EXECUTE",
        "COMPUTE, ALL, , 50000000, EXECUTE",
        "COMMUNICATION, ALL, , 1048576, ALL_REDUCE",
        "COMPUTE, ALL, , 30000000, EXECUTE",
    ]

    gpu_params: Dict[str, Any] = getattr(
        request,
        "param",
        {
            "gpu_id": 0,
            "instructions": instruction_list,
            "compute_tflops": 200,
            "chunk_size_bytes": 65536,
        },
    )
    return GPU(
        gpu_params["gpu_id"],
        gpu_params["instructions"],
        gpu_params["compute_tflops"],
        gpu_params["chunk_size_bytes"],
        network_instance,
        sim_engine_instance,
    )
