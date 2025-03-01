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

