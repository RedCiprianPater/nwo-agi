# NWO-AGI Supercomputer

Distributed AGI system for NWO Robotics. Connects robot fleets to form a collective supercomputer.

## Quick Start

### Install from GitHub (for now)
```bash
# Install directly from GitHub
pip install git+https://github.com/RedCiprianPater/nwo-agi.git

# Or clone and install locally
git clone https://github.com/RedCiprianPater/nwo-agi.git
cd nwo-agi
pip install -e .
```

### Connect your robot
```bash
# Using the CLI
nwo-agi --robot-id "ROBOT-001" --wallet "0x..." --gpu-memory 16 --ram 32

# Or run Python directly
python -m nwo_agi.cli --robot-id "ROBOT-001" --wallet "0x..."
```

### Python API
```python
from nwo_agi import NWOBridge, RobotHardware

# Configure your robot
hardware = RobotHardware(
    cpu_cores=8,
    gpu_cuda_cores=2048,
    gpu_memory_gb=16,
    ram_gb=32,
    robot_type="humanoid"
)

# Connect to the network
bridge = NWOBridge(
    robot_id="ROBOT-001",
    wallet="0x...",
    hardware=hardware
)

await bridge.start()
```

### PyPI Coming Soon
```bash
# Once published to PyPI (not yet available)
pip install nwo-agi
```

## Features

- 🤖 Robot hardware pooling
- 🧠 Distributed model inference
- 🎓 Collaborative training
- 💰 Compute earnings
- 🌐 P2P mesh networking

## Documentation

See [NWO-HYPERSPACE-INTEGRATION.md](docs/NWO-HYPERSPACE-INTEGRATION.md) for full details.
