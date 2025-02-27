from simulation_engine import SimulationEngine
from gpu import GPU
from network import Network

# Constants
NUM_GPUS = 3
BANDWIDTH = 100  # Assume no bandwidth sharing
NETWORK_ID = "network"

# Define instructions for each GPU
gpu_instructions = {
    0: [("compute", 5), ("communicate", 1, 500)],
    1: [("compute", 3), ("communicate", 2, 300)],
    2: [("compute", 4), ("communicate", 0, 400)]
}

# Initialize engine
engine = SimulationEngine()

# Create GPUs
gpus = {}
for gpu_id, instructions in gpu_instructions.items():
    gpus[gpu_id] = GPU(gpu_id, instructions, None, engine)

# Create Network and pass GPU references
network = Network(NETWORK_ID, BANDWIDTH, engine, gpus)

# Assign network to GPUs (fix circular dependency)
for gpu in gpus.values():
    gpu.network = network

# Register objects in the engine
for gpu_id, gpu in gpus.items():
    engine.register_object(gpu_id, gpu)
engine.register_object(NETWORK_ID, network)

# Start initial instructions for all GPUs
for gpu in gpus.values():
    gpu.start_next_instruction()

# Run the simulation
engine.run()
