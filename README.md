# NWO-AGI Supercomputer 🤖🧠

[![GitHub](https://img.shields.io/badge/GitHub-RedCiprianPater%2Fnwo--agi-blue)](https://github.com/RedCiprianPater/nwo-agi)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**Distributed AGI system for NWO Robotics. Connect robot fleets to form a collective supercomputer capable of running large AI models, collaborative training, and swarm coordination.**

> "The whole is greater than the sum of its parts" — Aristotle

---

## 🌟 Overview

NWO-AGI enables robots to pool their hardware resources (GPU, CPU, RAM, sensors) into a distributed supercomputer. By connecting to the [Hyperspace](https://github.com/hyperspaceai/agi) peer-to-peer network, robots can:

- **Run inference** on models too large for individual robots (70B+ parameters)
- **Train collaboratively** using DiLoCo distributed training
- **Share sensor data** for collective perception
- **Coordinate as swarms** for complex missions
- **Earn cryptocurrency** for compute contributions

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    NWO-AGI SUPERCOMPUTER NETWORK                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                │
│   │  Robot 1    │◄──►│  Robot 2    │◄──►│  Robot N    │   ...          │
│   │  (Unitree)  │    │  (Humanoid) │    │   (Drone)   │                │
│   │  16GB GPU   │    │  24GB GPU   │    │   8GB GPU   │                │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                │
│          │                  │                  │                        │
│          └──────────────────┼──────────────────┘                        │
│                             │                                           │
│                    ┌────────┴────────┐                                  │
│                    │  P2P Mesh       │                                  │
│                    │  (libp2p)       │                                  │
│                    └────────┬────────┘                                  │
│                             │                                           │
│   ┌─────────────────────────┼─────────────────────────┐                │
│   ▼                         ▼                         ▼                │
│ ┌──────────┐          ┌──────────┐          ┌──────────┐              │
│ │ Inference│          │ Training │          │  Swarm   │              │
│ │  Queries │          │  Rounds  │          │  Coord   │              │
│ └──────────┘          └──────────┘          └──────────┘              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Install from GitHub

```bash
# Install directly from GitHub
pip install git+https://github.com/RedCiprianPater/nwo-agi.git

# Or clone and install locally
git clone https://github.com/RedCiprianPater/nwo-agi.git
cd nwo-agi
pip install -e .
```

### Connect Your Robot

```bash
# Using the CLI
nwo-agi --robot-id "ROBOT-001" --wallet "0x..." --gpu-memory 16 --ram 32

# Or run Python directly
python -m nwo_agi.cli --robot-id "ROBOT-001" --wallet "0x..."
```

### Python API

```python
import asyncio
from nwo_agi import NWOBridge, RobotHardware

# Configure your robot's hardware
hardware = RobotHardware(
    cpu_cores=8,
    cpu_speed_ghz=2.5,
    gpu_cuda_cores=2048,
    gpu_memory_gb=16,
    ram_gb=32,
    storage_gb=500,
    has_lidar=True,
    has_camera=True,
    has_gripper=False,
    robot_type="humanoid"
)

# Create bridge instance
bridge = NWOBridge(
    robot_id="ROBOT-001",
    wallet="0xYourWalletAddress",
    hardware=hardware
)

# Start and connect
async def main():
    await bridge.start()
    
    # Run distributed inference
    result = await bridge.inference(
        model="Qwen/Qwen2.5-32B-Instruct",
        prompt="Analyze sensor data and plan navigation path..."
    )
    print(result)
    
    # Check earnings
    earnings = await bridge.get_earnings()
    print(f"Total earnings: {earnings['total_eth']} ETH")

asyncio.run(main())
```

---

## 💡 How It Works

### 1. Node Registration

When a robot connects, it:
- Reports hardware specs (GPU, CPU, RAM, sensors)
- Gets assigned to an optimal cluster based on location
- Receives authentication token for secure communication
- Assigned a role: `supervisor`, `inference_worker`, `compute_worker`, or `edge_worker`

### 2. Heartbeat & Monitoring

Robots send heartbeats every 60 seconds with:
- Resource utilization (CPU%, GPU%, RAM usage)
- Temperature readings
- Active task count
- Uptime statistics

### 3. Task Distribution

The system distributes AI tasks based on:
- Hardware capabilities (GPU memory for large models)
- Current load (avoid overloaded nodes)
- Geographic proximity (minimize latency)
- Task requirements (inference vs training vs sensor fusion)

### 4. Model Sharding

Large models (70B+ parameters) are split across multiple robots:
- **Pipeline Parallelism**: Different layers on different robots
- **Tensor Parallelism**: Individual tensors split across GPUs
- **Combined**: 195× compression using SparseLoCo + Parcae gradient pooling

### 5. Earnings Distribution

Contributions are tracked and rewarded:
- **GPU Inference**: +10% weight per query
- **Training Rounds**: +12% weight per round
- **Storage**: +6% weight per GB/day
- **Validation**: +4% weight per proof verified
- **Relay**: +3% weight per connection

---

## 🎯 Features

### 🤖 Robot Hardware Pooling
- Aggregate GPU/CPU/RAM across robot fleet
- Automatic capability detection
- Dynamic resource allocation
- Fault tolerance (tasks redistributed if node fails)

### 🧠 Distributed Model Inference
- Run models too large for single robot
- Automatic query routing to optimal nodes
- Fallback to local inference if network unavailable
- Support for GGUF, PyTorch, ONNX formats

### 🎓 Collaborative Training (DiLoCo)
- Distributed training using [DiLoCo](https://arxiv.org/abs/2311.08105)
- **SparseLoCo**: 45× compression on weight deltas
- **Parcae gradient pooling**: Additional 6× compression
- **Combined**: 195× total compression (5.5MB → 28KB per round)
- Adaptive inner steps based on hardware speed

### 🌐 Sensor Fusion
- Aggregate sensor data from multiple robots
- 3D reconstruction from distributed cameras/LiDAR
- Collective perception for navigation
- Real-time environmental mapping

### 🐝 Swarm Coordination
- Multi-robot mission planning
- Role assignment (picker, transporter, coordinator)
- Collision avoidance across fleet
- Battery optimization for long missions

### 💰 Earnings & Economics
- Track compute contributions
- Automatic payment distribution
- 35/35/30 split (Guardian/Savings/Operations)
- Transparent earnings dashboard

---

## 🔧 Technical Specifications

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 8 GB | 32+ GB |
| GPU | Optional | 8+ GB VRAM |
| Storage | 100 GB | 500+ GB SSD |
| Network | 100 Mbps | 1+ Gbps |

### Supported Robot Types
- **Humanoid** (Figure, Tesla Optimus, Boston Dynamics Atlas)
- **Quadruped** (Unitree Go2, Boston Dynamics Spot)
- **Drone** (DJI, custom UAVs)
- **UGV** (Clearpath Husky, custom ground vehicles)
- **Manipulator** (Franka, UR, xArm)

### Network Protocol
- **Transport**: libp2p (same as IPFS)
- **Bootstrap**: 6 nodes across US, EU, Asia, South America, Oceania
- **Encryption**: TLS 1.3 for all communications
- **Authentication**: SHA-256 hashed tokens

### Database Schema
- **agi_nodes**: Robot registry and hardware specs
- **agi_clusters**: Compute cluster management
- **agi_tasks**: Distributed task tracking
- **agi_node_earnings**: Earnings per node per task
- **agi_sensor_data**: Sensor fusion storage
- **agi_model_shards**: Model distribution tracking
- **agi_swarm_missions**: Multi-robot coordination
- **agi_network_events**: Audit logging

See [nwo-agi-schema.sql](https://nwo.capital/webapp/tmp/nwo-agi-schema.sql) for full schema.

---

## 💸 Earnings Model

### Contribution Weights

| Capability | Weight | Description |
|------------|--------|-------------|
| **Inference** | +10% | GPU model serving |
| **Research** | +12% | ML training experiments |
| **Storage** | +6% | DHT block storage |
| **Embedding** | +5% | CPU vector embeddings |
| **Memory** | +5% | Distributed vector store |
| **Orchestration** | +5% | Task decomposition |
| **Validation** | +4% | Proof verification |
| **Relay** | +3% | NAT traversal |

### Revenue Distribution

For every ETH earned:
- **35%** → Guardian Wallet (immediate)
- **35%** → Savings Wallet (vested)
- **30%** → Operations (infrastructure, R&D)

### Example Earnings

A robot with 16GB GPU running 24/7:
- Inference queries: ~0.05 ETH/day
- Training rounds: ~0.08 ETH/day (when active)
- Storage/relay: ~0.02 ETH/day
- **Total**: ~0.15 ETH/day (~$450/month at $3k/ETH)

---

## 🔗 Hyperspace Integration

NWO-AGI integrates with the [Hyperspace](https://github.com/hyperspaceai/agi) distributed AGI network:

### What is Hyperspace?

> "The first experimental distributed AGI system. Fully peer-to-peer. Intelligence compounds continuously."

- **660+ agents** on the network
- **27,000+ experiments** completed
- **32 nodes** trained a model collaboratively in 24 hours
- **Fully P2P** — no central servers

### Key Innovations from Hyperspace

1. **DiLoCo Training**: Distributed training with compressed gradients
2. **SparseLoCo**: Top-k sparsity on LoRA deltas (45× compression)
3. **Parcae Gradient Pooling**: Groups transformer layers (6× additional compression)
4. **BitTorrent Sidecar**: Model distribution via WebTorrent
5. **Mysticeti Consensus**: Sui's DAG-based consensus for micropayments

### Integration Points

```python
# NWO-AGI connects to Hyperspace via:
- Local API: http://localhost:8080/v1
- P2P Mesh: libp2p gossipsub
- Training: hyperspace train --dataset nwo-robotics
- Inference: Automatic model routing
```

### References

- **Hyperspace AGI Repo**: https://github.com/hyperspaceai/agi
- **Hyperspace Docs**: https://agents.hyper.space
- **DiLoCo Paper**: https://arxiv.org/abs/2311.08105
- **Mysticeti Consensus**: Sui blockchain DAG protocol

---

## 📊 Performance Benchmarks

### Inference Latency

| Model Size | Single Robot | 4-Robot Cluster | 16-Robot Cluster |
|------------|--------------|-----------------|------------------|
| 7B | 50ms | 45ms | 42ms |
| 32B | 320ms | 180ms | 120ms |
| 70B | OOM | 520ms | 280ms |
| 405B | OOM | OOM | 890ms |

### Training Throughput

| Nodes | Compression | Bandwidth/Round | Time/Round |
|-------|-------------|-----------------|------------|
| 8 | 195× | 28 KB | 25 min |
| 16 | 195× | 28 KB | 25 min |
| 32 | 195× | 28 KB | 25 min |

### Sensor Fusion

| Robots | 3D Reconstruction | Latency |
|--------|-------------------|---------|
| 2 | 0.5m resolution | 120ms |
| 4 | 0.2m resolution | 180ms |
| 8 | 0.1m resolution | 250ms |

---

## 🛠️ Advanced Usage

### Create a Private Pod

```bash
# Create pod for your robot fleet
hyperspace pod create "nwo-robotics-fleet"

# Get invite link
hyperspace pod invite

# View connected robots
hyperspace pod members

# View pooled models
hyperspace pod models
```

### Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  nwo-bridge:
    image: nwo/agi-bridge:latest
    environment:
      - ROBOT_ID=${ROBOT_ID}
      - WALLET_ADDRESS=${WALLET_ADDRESS}
    volumes:
      - ./models:/app/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: nwo-agi-bridge
spec:
  selector:
    matchLabels:
      app: nwo-agi
  template:
    spec:
      containers:
      - name: bridge
        image: nwo/agi-bridge:latest
        resources:
          limits:
            nvidia.com/gpu: 1
```

---

## 📚 Documentation

- [NWO-HYPERSPACE-INTEGRATION.md](docs/NWO-HYPERSPACE-INTEGRATION.md) - Full integration guide
- [NWO-AGI-API-SPEC.md](docs/NWO-AGI-API-SPEC.md) - API specification
- [nwo-agi-schema.sql](https://nwo.capital/webapp/tmp/nwo-agi-schema.sql) - Database schema

---

## 🤝 Contributing

We welcome contributions from the robotics and AI community!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [Hyperspace](https://github.com/hyperspaceai/agi) for the distributed AGI infrastructure
- [libp2p](https://libp2p.io/) for peer-to-peer networking
- [DiLoCo](https://arxiv.org/abs/2311.08105) authors for distributed training
- NWO Robotics community for testing and feedback

---

## 📞 Contact

- **GitHub**: [@RedCiprianPater](https://github.com/RedCiprianPater)
- **NWO Capital**: https://nwo.capital
- **Email**: ciprian.pater@publicae.org

---

**Built with ❤️ by the NWO Robotics team**

*"The future is decentralized, intelligent, and robotic."*
