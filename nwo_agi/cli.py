#!/usr/bin/env python3
"""CLI for NWO-AGI"""
import argparse
import asyncio
from .bridge import NWOBridge, RobotHardware

def main():
    parser = argparse.ArgumentParser(description="NWO-AGI Supercomputer")
    parser.add_argument("--robot-id", required=True, help="Robot ID")
    parser.add_argument("--wallet", required=True, help="Wallet address")
    parser.add_argument("--gpu-memory", type=int, default=16, help="GPU memory in GB")
    parser.add_argument("--ram", type=int, default=32, help="RAM in GB")
    
    args = parser.parse_args()
    
    hardware = RobotHardware(
        cpu_cores=8,
        cpu_speed_ghz=2.5,
        gpu_cuda_cores=2048,
        gpu_memory_gb=args.gpu_memory,
        ram_gb=args.ram,
        storage_gb=500,
        robot_type="generic"
    )
    
    bridge = NWOBridge(
        robot_id=args.robot_id,
        wallet=args.wallet,
        hardware=hardware
    )
    
    asyncio.run(bridge.start())

if __name__ == "__main__":
    main()
