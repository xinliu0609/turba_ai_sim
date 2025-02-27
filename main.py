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
    gpu_instructions = []
    print(instruction_lines)

    system_config_lines = read_input_files(system_config_file)
    bandwidth = 800 # Gbps
    num_gpus = 8
    print(system_config_lines)

    # Initialize the simulation engine
    engine = SimulationEngine()
    
    # Create and register network
    network = Network("network", bandwidth, engine)
    engine.register_object(num_gpus+1, network)

    # Create and register GPUs
    gpus = []
    for gpu_id in range(0, num_gpus):
        gpu = GPU(gpu_id, gpu_instructions, network, engine)
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
        gpu.start_next_instruction()

    # Run the simulation
    engine.run()
    

if __name__ == "__main__":
    main()