# turba_ai_sim
**Simple simulation prototype for AI training**

## 📜 **File & Directory Descriptions**

### **🔹 Core Modules**
- **[`simulation_engine.py`](./simulation_engine.py)** → Core event-driven simulation engine. Manages event queue and execution.
- **[`gpu.py`](./gpu.py)** → Defines the `GPU` class. Handles compute and communication events.
- **[`network.py`](./network.py)** → Defines the `Network` class. Models data transfer and bandwidth sharing.
- **[`main.py`](./main.py)** → Entry point to start the simulation. Loads configurations and initializes components.

### **🔹 Testing**
- **[`tests/`](./tests/)** → Contains all test scripts for unit testing with `pytest`.
- **[`tests/conftest.py`](./tests/conftest.py)** → Defines shared test fixtures for `pytest`.

### **🔹 Configuration & Documentation**
- **[`system_config.txt`](./system_config.txt)** → Specify system configuration.
- **[`gpu_trace.txt`](./gpu_trace.txt)** → Specify computing and communication instructions for all GPUs.
- **[`README.md`](./README.md)** → Project documentation. You’re reading it now!

### **🔹 Miscellaneous**
- **[`.gitignore`](./.gitignore)** → Specifies files that should be ignored by Git (e.g., `.pyc`, `__pycache__`).
- **[`.mypy.ini`](./mypy.ini)** → Specifies the rules for type checking with `mypy`.

---

## 🚀 **Getting Started**

### **1️⃣ Install Dependencies**

If your project has dependencies, install them using:

```bash
pip install black
pip install mypy
pip install pytest
```

### **2️⃣ Run the Simulator**

To start the simulation, do the following:
- update **[`system_config.txt`](./system_config.txt)** and **[`gpu_trace.txt`](./gpu_trace.txt)** according to your setup
- run the command:

```bash
python main.py
```

The sample output looks like:
```
get object id = 8
GPU 0 started computing at 0
GPU 1 started computing at 0
GPU 2 started computing at 0
GPU 3 started computing at 0
GPU 4 started computing at 0
GPU 5 started computing at 0
GPU 6 started computing at 0
GPU 7 started computing at 0
Network: GPU 0 starts sending 1048576 data to all other GPUs
Network: GPU 2 starts sending 1048576 data to all other GPUs
Network: GPU 6 starts sending 1048576 data to all other GPUs
Network: GPU 5 starts sending 1048576 data to all other GPUs
Network: GPU 1 starts sending 1048576 data to all other GPUs
Network: GPU 4 starts sending 1048576 data to all other GPUs
Network: GPU 3 starts sending 1048576 data to all other GPUs
Network: GPU 7 starts sending 1048576 data to all other GPUs
...
GPU 0 finished computing at 150
GPU 5 finished computing at 500
GPU 5 started computing at 0
GPU 5 finished computing at 250
GPU 5 started computing at 0
GPU 5 finished computing at 150
GPU 7 finished comm at 41944
GPU 1 finished comm at 41944
GPU 6 finished comm at 41944
GPU 2 finished comm at 41944
GPU 5 finished comm at 41944
GPU 4 finished comm at 41944
GPU 0 finished comm at 41944
GPU 3 finished comm at 41944
Simulation completed.
```

### **3️⃣ Run Unit Tests**

To verify the implementation:

```bash
pytest
```

### **4️⃣ Auto formatting and type check**

After making changes to the files, run:

```bash
black .
mypy .
```