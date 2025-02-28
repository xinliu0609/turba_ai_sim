from simulation_engine import SimulationEngine
from gpu import GPU
from network import Network


def read_input_files(file_path):
    """Read the text config file, exclude comments and whitespace
    
    Rules:
    - Lines starting with '#' are ignored.
    - Empty lines are ignored.
    - Lines with '#' elsewhere keep only the part before '#'.
    """
    valid_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            # Remove leading/trailing whitespace
            line = line.strip()
            if not line:
                continue

            if line.startswith("#"):
                continue

            if "#" in line:
                line = line.split("#", 1)[0].strip()

            if line:
                valid_lines.append(line)

    return valid_lines


def initialize_simulation(trace_file, system_config_file):
    """Initializes the simulation engine, GPUs, and network."""
    
    # read gpu trace file and produce instructions for each GPU
    instruction_lines = read_input_files(trace_file)
    system_config_lines = read_input_files(system_config_file)
    config_dict = {}
    for line in system_config_lines:
        if ":" in line:
            key, value = line.split(":", 1) # max 1 split
            key = key.strip()
            value = value.strip()
            config_dict[key] = value
        else:
            raise ValueError(f"system_config.txt has an error line: {line}")

    num_gpus = int(config_dict["NUM_GPUS"])
    bandwidth_gbps = int(config_dict["NETWORK_BANDWIDTH"])
    topology = config_dict["TOPOLOGY"]
    compute_tflops = int(config_dict["COMPUTE_CAPABILITY"])
    chunk_size_bytes = int(config_dict["COMMUNICATION_CHUNK_SIZE"])

    # Initialize the simulation engine
    engine = SimulationEngine()
    
    # Create and register network
    network = Network(num_gpus, num_gpus, bandwidth_gbps, topology, engine)
    engine.register_object(network.object_id, network)

    # Create and register GPUs
    gpus = []
    for gpu_id in range(0, num_gpus):
        gpu = GPU(gpu_id, instruction_lines, compute_tflops, chunk_size_bytes, network, engine)
        engine.register_object(gpu_id, gpu)
        gpus.append(gpu)

    return engine, gpus


def main():
    """Main function to run the simulation."""
    system_config_file = "system_config.txt"
    trace_file = "gpu_trace.txt"

    # Read input and initialize simulation
    engine, gpus = initialize_simulation(trace_file, system_config_file)

    # Start initial instructions for all GPUs
    for gpu in gpus:
        gpu.start_gpu()

    # Run the simulation
    engine.run()
    

if __name__ == "__main__":
    main()