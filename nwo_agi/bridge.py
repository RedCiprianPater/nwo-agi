#!/usr/bin/env python3
"""
NWO-Hyperspace Bridge
Connects NWO robots to the Hyperspace AGI network
"""

import asyncio
import json
import logging
import subprocess
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('nwo-hyperspace')

@dataclass
class RobotHardware:
    """Hardware capabilities of the robot"""
    cpu_cores: int
    cpu_speed_ghz: float
    gpu_cuda_cores: int
    gpu_memory_gb: int
    ram_gb: int
    storage_gb: int
    has_lidar: bool = False
    has_camera: bool = False
    has_gripper: bool = False
    robot_type: str = "generic"  # 'humanoid', 'quadruped', 'drone', 'ugv'

@dataclass
class NodeCapabilities:
    """Capabilities this node can provide to Hyperspace"""
    inference: bool = False
    research: bool = False
    embedding: bool = True
    storage: bool = True
    validation: bool = True
    relay: bool = True

class NWOBridge:
    """
    Bridge between NWO Robotics and Hyperspace AGI network
    """
    
    def __init__(self, robot_id: str, wallet: str, hardware: RobotHardware, 
                 nwo_api_base: str = "https://nwo.capital/webapp/api"):
        self.robot_id = robot_id
        self.wallet = wallet
        self.hardware = hardware
        self.nwo_api_base = nwo_api_base
        self.capabilities = self._determine_capabilities()
        self.hyperspace_pid = None
        self.hyperspace_api = "http://localhost:8080"
        self.nwo_node_id = None
        self.nwo_auth_token = None
        self.running = False
        
    def _determine_capabilities(self) -> NodeCapabilities:
        """Determine what capabilities this robot can provide"""
        caps = NodeCapabilities()
        
        # GPU inference if we have CUDA cores
        if self.hardware.gpu_cuda_cores > 512:
            caps.inference = True
            logger.info(f"GPU inference enabled ({self.hardware.gpu_cuda_cores} CUDA cores)")
            
        # Research if we have significant GPU
        if self.hardware.gpu_memory_gb >= 8:
            caps.research = True
            logger.info(f"Research training enabled ({self.hardware.gpu_memory_gb}GB GPU memory)")
            
        return caps
    
    async def start(self):
        """Start the Hyperspace CLI and connect to network"""
        logger.info(f"🚀 Starting NWO-Hyperspace Bridge for {self.robot_id}")
        
        # Install Hyperspace CLI if not present
        await self._ensure_hyperspace_cli()
        
        # Start Hyperspace daemon
        self.hyperspace_pid = await self._start_hyperspace_daemon()
        
        # Configure node capabilities
        await self._configure_capabilities()
        
        # Register with NWO AGI API
        await self._register_with_nwo()
        
        self.running = True
        logger.info("✅ Bridge started successfully")
        
        # Start heartbeat loop
        asyncio.create_task(self._heartbeat_loop())
        
    async def _ensure_hyperspace_cli(self):
        """Install Hyperspace CLI if not already installed"""
        try:
            result = subprocess.run(
                ["hyperspace", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            logger.info(f"✓ Hyperspace CLI found: {result.stdout.strip()}")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            logger.info("📥 Installing Hyperspace CLI...")
            try:
                subprocess.run([
                    "bash", "-c",
                    "curl -fsSL https://agents.hyper.space/api/install | bash"
                ], check=True, timeout=120)
                logger.info("✓ Hyperspace CLI installed")
            except Exception as e:
                logger.error(f"Failed to install Hyperspace CLI: {e}")
                raise
            
    async def _start_hyperspace_daemon(self) -> int:
        """Start the Hyperspace daemon process"""
        logger.info("🔄 Starting Hyperspace daemon...")
        
        # Start hyperspace in background
        process = subprocess.Popen(
            ["hyperspace", "start", "--daemon"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )
        
        logger.info(f"✓ Hyperspace daemon started (PID: {process.pid})")
        
        # Wait for API to be ready
        await asyncio.sleep(5)
        
        # Verify it's running
        for i in range(10):
            try:
                response = requests.get(
                    f"{self.hyperspace_api}/v1/health",
                    timeout=5
                )
                if response.status_code == 200:
                    logger.info("✓ Hyperspace API is ready")
                    break
            except:
                await asyncio.sleep(2)
        
        return process.pid
    
    async def _configure_capabilities(self):
        """Configure which capabilities this node provides"""
        caps = self.capabilities
        logger.info("⚙️ Configuring capabilities...")
        
        # Enable inference if we have GPU
        if caps.inference:
            try:
                subprocess.run(
                    ["hyperspace", "config", "set", "inference.enabled", "true"],
                    check=True, timeout=10
                )
                
                # Load a model for inference
                logger.info("📦 Loading inference model...")
                subprocess.run(
                    ["hyperspace", "model", "load", "Qwen/Qwen2.5-7B-Instruct-GGUF"],
                    check=True, timeout=60
                )
                logger.info("✓ Model loaded")
            except Exception as e:
                logger.warning(f"Could not configure inference: {e}")
        
        # Enable research if capable
        if caps.research:
            try:
                subprocess.run(
                    ["hyperspace", "config", "set", "research.enabled", "true"],
                    check=True, timeout=10
                )
                logger.info("✓ Research training enabled")
            except Exception as e:
                logger.warning(f"Could not configure research: {e}")
            
        logger.info(f"✓ Capabilities configured: {caps}")
        
    async def _register_with_nwo(self):
        """Register this robot with the NWO AGI API"""
        logger.info("📝 Registering with NWO AGI API...")
        
        registration_data = {
            "robot_id": self.robot_id,
            "wallet": self.wallet,
            "hardware": {
                "cpu_cores": self.hardware.cpu_cores,
                "cpu_speed_ghz": self.hardware.cpu_speed_ghz,
                "gpu_cuda_cores": self.hardware.gpu_cuda_cores,
                "gpu_memory_gb": self.hardware.gpu_memory_gb,
                "ram_gb": self.hardware.ram_gb,
                "storage_gb": self.hardware.storage_gb,
            },
            "capabilities": [
                cap for cap, enabled in self.capabilities.__dict__.items()
                if enabled
            ],
            "sensors": {
                "lidar": self.hardware.has_lidar,
                "camera": self.hardware.has_camera,
                "gripper": self.hardware.has_gripper,
            },
            "robot_type": self.hardware.robot_type,
            "hyperspace_node": True
        }
        
        try:
            response = requests.post(
                f"{self.nwo_api_base}/agi-node.php?action=register",
                json=registration_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    self.nwo_node_id = data['node_id']
                    self.nwo_auth_token = data['auth_token']
                    logger.info(f"✅ Registered with NWO: {self.nwo_node_id}")
                    logger.info(f"   Cluster: {data.get('cluster_id')}")
                    logger.info(f"   Role: {data.get('assigned_role')}")
                else:
                    logger.error(f"NWO registration failed: {data.get('error')}")
            else:
                logger.error(f"NWO registration failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"NWO registration error: {e}")
    
    async def _heartbeat_loop(self):
        """Send periodic heartbeats to NWO"""
        while self.running:
            try:
                await self._send_heartbeat()
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                
            await asyncio.sleep(60)  # Heartbeat every minute
    
    async def _send_heartbeat(self):
        """Send heartbeat with current status"""
        if not self.nwo_node_id or not self.nwo_auth_token:
            return
            
        # Get resource usage
        resources = await self._get_resource_usage()
        
        try:
            response = requests.post(
                f"{self.nwo_api_base}/agi-node.php?action=heartbeat",
                json={
                    "node_id": self.nwo_node_id,
                    "auth_token": self.nwo_auth_token,
                    "resources": resources,
                    "status": "healthy",
                    "uptime_seconds": await self._get_uptime()
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('assigned_tasks'):
                    logger.info(f"📋 Assigned tasks: {len(data['assigned_tasks'])}")
                    
        except Exception as e:
            logger.warning(f"Failed to send heartbeat: {e}")
    
    async def _get_resource_usage(self) -> Dict:
        """Get current resource usage of the robot"""
        try:
            import psutil
            
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "ram_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
                "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "gpu_percent": await self._get_gpu_usage(),
                "temperature_c": await self._get_temperature(),
                "active_tasks": len(await self._get_active_tasks())
            }
        except ImportError:
            logger.warning("psutil not installed, using default values")
            return {
                "cpu_percent": 0,
                "ram_used_gb": 0,
                "ram_total_gb": self.hardware.ram_gb,
                "gpu_percent": 0,
                "temperature_c": 45,
                "active_tasks": 0
            }
    
    async def _get_gpu_usage(self) -> float:
        """Get GPU utilization if available"""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=utilization.gpu", 
                 "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return float(result.stdout.strip())
        except:
            return 0.0
    
    async def _get_temperature(self) -> float:
        """Get robot temperature"""
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                return int(f.read().strip()) / 1000.0
        except:
            return 45.0
    
    async def _get_active_tasks(self) -> List[Dict]:
        """Get list of active compute tasks"""
        try:
            response = requests.get(
                f"{self.hyperspace_api}/v1/tasks",
                timeout=5
            )
            return response.json().get('tasks', [])
        except:
            return []
    
    async def _get_uptime(self) -> int:
        """Get system uptime in seconds"""
        try:
            with open('/proc/uptime', 'r') as f:
                return int(float(f.read().split()[0]))
        except:
            return 0
    
    async def inference(self, model: str, prompt: str, **kwargs) -> Dict:
        """
        Run inference using Hyperspace network
        Falls back to local if network unavailable
        """
        logger.info(f"🤖 Running inference with {model}")
        
        try:
            # Try Hyperspace network first
            response = requests.post(
                f"{self.hyperspace_api}/v1/chat/completions",
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    **kwargs
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "source": "hyperspace_network",
                    "result": response.json(),
                    "robot_id": self.robot_id
                }
                
        except Exception as e:
            logger.warning(f"Hyperspace inference failed: {e}, falling back to local")
        
        # Fallback to local NWO inference
        return await self._local_inference(model, prompt, **kwargs)
    
    async def _local_inference(self, model: str, prompt: str, **kwargs) -> Dict:
        """Run inference locally using NWO robotics API"""
        try:
            response = requests.post(
                f"{self.nwo_api_base}/robotics.php",
                json={
                    "action": "inference",
                    "model": model,
                    "prompt": prompt,
                    "robot_id": self.robot_id
                },
                timeout=30
            )
            
            return {
                "source": "nwo_local",
                "result": response.json(),
                "robot_id": self.robot_id
            }
            
        except Exception as e:
            logger.error(f"Local inference failed: {e}")
            return {"error": str(e), "robot_id": self.robot_id}
    
    async def train_collaborative(self, dataset: str, model_config: Optional[Dict] = None):
        """
        Join collaborative training round on Hyperspace
        """
        logger.info(f"🎓 Joining collaborative training for dataset: {dataset}")
        
        try:
            # Start training worker
            process = subprocess.Popen(
                ["hyperspace", "train", "--dataset", dataset],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Monitor progress
            while process.poll() is None:
                stdout = process.stdout.readline()
                if stdout:
                    line = stdout.decode().strip()
                    if line:
                        logger.info(f"Training: {line}")
                await asyncio.sleep(1)
            
            logger.info("✅ Training round completed")
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
    
    async def get_earnings(self) -> Dict:
        """Get earnings from compute contributions"""
        try:
            # Query Hyperspace for earnings
            hyperspace_earnings = {"total": 0}
            try:
                response = requests.get(
                    f"{self.hyperspace_api}/v1/earnings",
                    timeout=10
                )
                if response.status_code == 200:
                    hyperspace_earnings = response.json()
            except:
                pass
            
            # Query NWO for earnings
            nwo_earnings = 0
            if self.nwo_node_id:
                try:
                    response = requests.get(
                        f"{self.nwo_api_base}/agi-node.php?action=status&node_id={self.nwo_node_id}",
                        timeout=10
                    )
                    if response.status_code == 200:
                        data = response.json()
                        nwo_earnings = data.get('node', {}).get('total_earnings_eth', 0)
                except:
                    pass
            
            return {
                "hyperspace": hyperspace_earnings,
                "nwo": nwo_earnings,
                "total_eth": hyperspace_earnings.get('total', 0) + nwo_earnings,
                "robot_id": self.robot_id
            }
            
        except Exception as e:
            logger.error(f"Failed to get earnings: {e}")
            return {"error": str(e), "robot_id": self.robot_id}
    
    async def stop(self):
        """Stop the bridge gracefully"""
        logger.info("🛑 Stopping NWO-Hyperspace Bridge...")
        self.running = False
        
        if self.hyperspace_pid:
            try:
                subprocess.run(["kill", str(self.hyperspace_pid)], check=False)
                logger.info("✓ Hyperspace daemon stopped")
            except:
                pass
        
        logger.info("✅ Bridge stopped")


# Example usage
async def main():
    """Example: Connect a Unitree robot to Hyperspace"""
    
    # Define robot hardware
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
        robot_type="quadruped"
    )
    
    # Create bridge
    bridge = NWOBridge(
        robot_id="UNITREE-GO2-001",
        wallet="0x...",  # Replace with actual wallet
        hardware=hardware
    )
    
    # Start bridge
    await bridge.start()
    
    # Example: Run inference
    result = await bridge.inference(
        model="Qwen/Qwen2.5-7B-Instruct",
        prompt="Analyze this sensor data and suggest navigation path..."
    )
    print(f"Inference result: {json.dumps(result, indent=2)}")
    
    # Keep running and show earnings periodically
    try:
        while True:
            await asyncio.sleep(300)  # Every 5 minutes
            earnings = await bridge.get_earnings()
            print(f"💰 Total earnings: {earnings.get('total_eth', 0):.6f} ETH")
    except KeyboardInterrupt:
        await bridge.stop()


if __name__ == "__main__":
    asyncio.run(main())
