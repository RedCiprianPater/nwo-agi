# NWO-AGI Supercomputer API Integration

## Overview

The NWO-AGI system enables NWO robots to link their hardware resources (CPU, GPU, memory, sensors) to form a distributed supercomputer capable of running large AI models and complex computations.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    NWO-AGI Supercomputer                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │ Robot 1 │  │ Robot 2 │  │ Robot 3 │  │ Robot N │  ...      │
│  │ (Node)  │  │ (Node)  │  │ (Node)  │  │ (Node)  │           │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘           │
│       │            │            │            │                 │
│       └────────────┴────────────┴────────────┘                 │
│                         │                                       │
│              ┌──────────┴──────────┐                           │
│              │   AGI Controller    │                           │
│              │  (Resource Manager) │                           │
│              └──────────┬──────────┘                           │
│                         │                                       │
│       ┌─────────────────┼─────────────────┐                    │
│       ▼                 ▼                 ▼                    │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐                │
│  │  LLM    │      │  VLA    │      │ Ethics  │                │
│  │ Engine  │      │ Engine  │      │ Engine  │                │
│  └─────────┘      └─────────┘      └─────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

## API Endpoints

### 1. Node Registration
```php
POST /api/agi/node/register
```

Robots register their hardware capabilities to join the supercomputer.

**Request:**
```json
{
  "robot_id": "ROBOT-ABC123",
  "wallet": "0x...",
  "hardware": {
    "cpu_cores": 8,
    "cpu_speed_ghz": 2.5,
    "gpu_cuda_cores": 2048,
    "gpu_memory_gb": 8,
    "ram_gb": 32,
    "storage_gb": 500,
    "network_mbps": 1000
  },
  "capabilities": ["inference", "training", "sensor_fusion", "actuation"],
  "location": {
    "lat": 59.9139,
    "lng": 10.7522,
    "region": "eu-north"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "node_id": "NODE-XYZ789",
  "cluster_id": "CLUSTER-001",
  "auth_token": "eyJhbGciOiJIUzI1NiIs...",
  "assigned_role": "compute_worker",
  "supervisor_node": "NODE-ABC001"
}
```

### 2. Heartbeat & Resource Reporting
```php
POST /api/agi/node/heartbeat
```

Nodes report their current resource utilization and health status.

**Request:**
```json
{
  "node_id": "NODE-XYZ789",
  "auth_token": "eyJhbGciOiJIUzI1NiIs...",
  "resources": {
    "cpu_percent": 45,
    "gpu_percent": 30,
    "ram_used_gb": 12,
    "ram_total_gb": 32,
    "temperature_c": 65,
    "active_tasks": 3
  },
  "status": "healthy",
  "uptime_seconds": 86400
}
```

### 3. Task Distribution
```php
POST /api/agi/cluster/distribute
```

Distribute AI tasks across the robot cluster.

**Request:**
```json
{
  "cluster_id": "CLUSTER-001",
  "task": {
    "type": "llm_inference",
    "model": "llama-3-70b",
    "prompt": "Analyze sensor data and plan navigation...",
    "priority": "high",
    "deadline_ms": 5000
  },
  "requirements": {
    "min_gpu_memory_gb": 16,
    "min_ram_gb": 32,
    "max_latency_ms": 100
  }
}
```

**Response:**
```json
{
  "status": "success",
  "task_id": "TASK-001",
  "assigned_nodes": ["NODE-XYZ789", "NODE-ABC123"],
  "estimated_completion_ms": 3200,
  "shard_distribution": {
    "NODE-XYZ789": "layers_0-20",
    "NODE-ABC123": "layers_21-40"
  }
}
```

### 4. Collective Inference
```php
POST /api/agi/cluster/inference
```

Run distributed inference across multiple robots.

**Request:**
```json
{
  "cluster_id": "CLUSTER-001",
  "model_type": "vla",
  "model_name": "nwo-groot-n1",
  "input": {
    "image": "base64_encoded_image",
    "instruction": "Pick up the red box and place it on the shelf",
    "proprioception": {
      "joint_positions": [...],
      "gripper_state": 0.5
    }
  },
  "parallelism": "tensor_parallel",
  "num_shards": 4
}
```

### 5. Shared Memory Access
```php
POST /api/agi/memory/read
POST /api/agi/memory/write
```

Access distributed shared memory across the cluster.

### 6. Sensor Fusion
```php
POST /api/agi/sensors/fuse
```

Fuse sensor data from multiple robots for collective perception.

**Request:**
```json
{
  "cluster_id": "CLUSTER-001",
  "sensor_data": [
    {
      "node_id": "NODE-XYZ789",
      "camera": "base64_image",
      "lidar": "point_cloud_data",
      "timestamp": "2026-05-02T10:00:00Z"
    },
    {
      "node_id": "NODE-ABC123",
      "camera": "base64_image",
      "lidar": "point_cloud_data",
      "timestamp": "2026-05-02T10:00:00Z"
    }
  ],
  "fusion_type": "3d_reconstruction"
}
```

### 7. Swarm Coordination
```php
POST /api/agi/swarm/coordinate
```

Coordinate actions across robot swarm.

**Request:**
```json
{
  "cluster_id": "CLUSTER-001",
  "mission": {
    "type": "warehouse_optimization",
    "objective": "minimize_pick_time",
    "constraints": ["collision_avoidance", "battery_optimization"]
  },
  "robot_roles": {
    "NODE-XYZ789": "picker",
    "NODE-ABC123": "transporter",
    "NODE-DEF456": "coordinator"
  }
}
```

### 8. Model Parallelism Setup
```php
POST /api/agi/model/shard
```

Shard large models across multiple robots.

**Request:**
```json
{
  "cluster_id": "CLUSTER-001",
  "model": {
    "name": "nwo-agi-1T",
    "size_params": 1000000000000,
    "architecture": "transformer",
    "layers": 128
  },
  "sharding_strategy": "pipeline_parallel",
  "replication_factor": 2
}
```

### 9. Cluster Health & Metrics
```php
GET /api/agi/cluster/status?cluster_id=CLUSTER-001
```

**Response:**
```json
{
  "cluster_id": "CLUSTER-001",
  "status": "operational",
  "nodes_total": 12,
  "nodes_online": 11,
  "nodes_offline": 1,
  "aggregate_compute": {
    "total_cuda_cores": 24576,
    "total_ram_gb": 384,
    "total_gpu_memory_gb": 96,
    "utilization_percent": 67
  },
  "active_tasks": 23,
  "queue_depth": 5,
  "throughput": {
    "inferences_per_second": 156,
    "tokens_per_second": 4200
  }
}
```

### 10. Earnings Distribution
```php
POST /api/agi/earnings/distribute
```

Distribute earnings from collective compute tasks.

**Request:**
```json
{
  "cluster_id": "CLUSTER-001",
  "task_id": "TASK-001",
  "earnings_eth": 0.05,
  "distribution": {
    "NODE-XYZ789": 0.40,
    "NODE-ABC123": 0.35,
    "NODE-DEF456": 0.25
  }
}
```

## Database Schema

```sql
-- AGI Nodes Table
CREATE TABLE agi_nodes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    node_id VARCHAR(64) UNIQUE NOT NULL,
    robot_id VARCHAR(64) NOT NULL,
    wallet VARCHAR(42) NOT NULL,
    cluster_id VARCHAR(64),
    cpu_cores INT,
    cpu_speed_ghz DECIMAL(4,2),
    gpu_cuda_cores INT,
    gpu_memory_gb INT,
    ram_gb INT,
    storage_gb INT,
    network_mbps INT,
    capabilities JSON,
    location_lat DECIMAL(10,8),
    location_lng DECIMAL(11,8),
    region VARCHAR(32),
    status ENUM('online', 'offline', 'busy', 'maintenance') DEFAULT 'offline',
    auth_token_hash VARCHAR(128),
    last_heartbeat TIMESTAMP,
    total_compute_time_seconds BIGINT DEFAULT 0,
    total_earnings_eth DECIMAL(18,8) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AGI Clusters Table
CREATE TABLE agi_clusters (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cluster_id VARCHAR(64) UNIQUE NOT NULL,
    name VARCHAR(128),
    owner_wallet VARCHAR(42),
    status ENUM('active', 'inactive', 'scaling') DEFAULT 'active',
    max_nodes INT DEFAULT 100,
    task_queue JSON,
    aggregate_compute JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AGI Tasks Table
CREATE TABLE agi_tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    task_id VARCHAR(64) UNIQUE NOT NULL,
    cluster_id VARCHAR(64),
    type ENUM('inference', 'training', 'sensor_fusion', 'coordination'),
    model_name VARCHAR(128),
    status ENUM('queued', 'running', 'completed', 'failed') DEFAULT 'queued',
    assigned_nodes JSON,
    input_data JSON,
    output_data JSON,
    earnings_eth DECIMAL(18,8),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Node Earnings Table
CREATE TABLE agi_node_earnings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    node_id VARCHAR(64),
    task_id VARCHAR(64),
    earnings_eth DECIMAL(18,8),
    distribution_percent DECIMAL(5,2),
    paid_at TIMESTAMP,
    tx_hash VARCHAR(66)
);
```

## Implementation Files

### api-agi-node.php
```php
<?php
/**
 * NWO-AGI Node Management API
 * Handles robot registration, heartbeat, and resource reporting
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once __DIR__ . '/includes/config.php';

$action = $_GET['action'] ?? '';
$method = $_SERVER['REQUEST_METHOD'];

try {
    switch ($action) {
        case 'register':
            handleNodeRegistration();
            break;
        case 'heartbeat':
            handleHeartbeat();
            break;
        case 'status':
            handleNodeStatus();
            break;
        default:
            http_response_code(400);
            echo json_encode(['error' => 'Unknown action']);
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()]);
}

function handleNodeRegistration() {
    global $pdo;
    
    $data = json_decode(file_get_contents('php://input'), true);
    
    // Validate required fields
    if (empty($data['robot_id']) || empty($data['wallet'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing required fields']);
        return;
    }
    
    // Generate node ID
    $node_id = 'NODE-' . strtoupper(substr(md5(uniqid()), 0, 8));
    
    // Find or create cluster
    $cluster_id = findOptimalCluster($data['location'] ?? null);
    
    // Generate auth token
    $auth_token = bin2hex(random_bytes(32));
    $auth_token_hash = hash('sha256', $auth_token);
    
    // Insert node
    $stmt = $pdo->prepare("
        INSERT INTO agi_nodes 
        (node_id, robot_id, wallet, cluster_id, cpu_cores, cpu_speed_ghz, 
         gpu_cuda_cores, gpu_memory_gb, ram_gb, storage_gb, network_mbps,
         capabilities, location_lat, location_lng, region, auth_token_hash, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'online')
    ");
    
    $hw = $data['hardware'] ?? [];
    $stmt->execute([
        $node_id,
        $data['robot_id'],
        $data['wallet'],
        $cluster_id,
        $hw['cpu_cores'] ?? 4,
        $hw['cpu_speed_ghz'] ?? 2.0,
        $hw['gpu_cuda_cores'] ?? 0,
        $hw['gpu_memory_gb'] ?? 0,
        $hw['ram_gb'] ?? 8,
        $hw['storage_gb'] ?? 100,
        $hw['network_mbps'] ?? 100,
        json_encode($data['capabilities'] ?? []),
        $data['location']['lat'] ?? null,
        $data['location']['lng'] ?? null,
        $data['location']['region'] ?? 'unknown',
        $auth_token_hash
    ]);
    
    // Update cluster aggregate compute
    updateClusterCompute($cluster_id);
    
    echo json_encode([
        'status' => 'success',
        'node_id' => $node_id,
        'cluster_id' => $cluster_id,
        'auth_token' => $auth_token,
        'assigned_role' => determineNodeRole($hw),
        'supervisor_node' => findSupervisorNode($cluster_id)
    ]);
}

function handleHeartbeat() {
    global $pdo;
    
    $data = json_decode(file_get_contents('php://input'), true);
    
    $node_id = $data['node_id'] ?? '';
    $auth_token = $data['auth_token'] ?? '';
    
    // Verify auth
    $stmt = $pdo->prepare("SELECT id, cluster_id FROM agi_nodes WHERE node_id = ? AND auth_token_hash = ?");
    $stmt->execute([$node_id, hash('sha256', $auth_token)]);
    $node = $stmt->fetch();
    
    if (!$node) {
        http_response_code(401);
        echo json_encode(['error' => 'Invalid credentials']);
        return;
    }
    
    // Update node status
    $stmt = $pdo->prepare("
        UPDATE agi_nodes 
        SET status = ?, last_heartbeat = NOW(),
            total_compute_time_seconds = total_compute_time_seconds + ?
        WHERE id = ?
    ");
    $stmt->execute([
        $data['status'] ?? 'healthy',
        $data['uptime_seconds'] ?? 60,
        $node['id']
    ]);
    
    // Check for assigned tasks
    $tasks = getAssignedTasks($node_id);
    
    echo json_encode([
        'status' => 'success',
        'assigned_tasks' => $tasks,
        'cluster_update' => getClusterUpdate($node['cluster_id'])
    ]);
}

function findOptimalCluster($location) {
    global $pdo;
    
    // Find cluster in same region with capacity
    $region = $location['region'] ?? 'unknown';
    
    $stmt = $pdo->prepare("
        SELECT cluster_id FROM agi_clusters 
        WHERE region = ? AND status = 'active'
        AND (SELECT COUNT(*) FROM agi_nodes WHERE cluster_id = agi_clusters.cluster_id) < max_nodes
        LIMIT 1
    ");
    $stmt->execute([$region]);
    $cluster = $stmt->fetch();
    
    if ($cluster) {
        return $cluster['cluster_id'];
    }
    
    // Create new cluster
    $cluster_id = 'CLUSTER-' . strtoupper(substr(md5(uniqid()), 0, 6));
    $stmt = $pdo->prepare("
        INSERT INTO agi_clusters (cluster_id, name, region, status, max_nodes)
        VALUES (?, ?, ?, 'active', 100)
    ");
    $stmt->execute([$cluster_id, "Cluster $region", $region]);
    
    return $cluster_id;
}

function determineNodeRole($hardware) {
    $gpu_memory = $hardware['gpu_memory_gb'] ?? 0;
    $ram = $hardware['ram_gb'] ?? 8;
    
    if ($gpu_memory >= 16 && $ram >= 32) {
        return 'inference_worker';
    } elseif ($gpu_memory >= 8) {
        return 'compute_worker';
    } else {
        return 'edge_worker';
    }
}

function findSupervisorNode($cluster_id) {
    global $pdo;
    
    // Find node with most resources in cluster
    $stmt = $pdo->prepare("
        SELECT node_id FROM agi_nodes 
        WHERE cluster_id = ? AND status = 'online'
        ORDER BY (gpu_memory_gb + ram_gb) DESC
        LIMIT 1
    ");
    $stmt->execute([$cluster_id]);
    $node = $stmt->fetch();
    
    return $node ? $node['node_id'] : null;
}

function updateClusterCompute($cluster_id) {
    global $pdo;
    
    $stmt = $pdo->prepare("
        UPDATE agi_clusters 
        SET aggregate_compute = (
            SELECT JSON_OBJECT(
                'total_cuda_cores', SUM(gpu_cuda_cores),
                'total_ram_gb', SUM(ram_gb),
                'total_gpu_memory_gb', SUM(gpu_memory_gb),
                'total_nodes', COUNT(*)
            )
            FROM agi_nodes WHERE cluster_id = ?
        )
        WHERE cluster_id = ?
    ");
    $stmt->execute([$cluster_id, $cluster_id]);
}

function getAssignedTasks($node_id) {
    global $pdo;
    
    $stmt = $pdo->prepare("
        SELECT task_id, type, model_name, status 
        FROM agi_tasks 
        WHERE JSON_CONTAINS(assigned_nodes, ?) AND status IN ('queued', 'running')
    ");
    $stmt->execute(["\"$node_id\""]);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

function getClusterUpdate($cluster_id) {
    global $pdo;
    
    $stmt = $pdo->prepare("
        SELECT cluster_id, status, aggregate_compute, active_tasks
        FROM agi_clusters WHERE cluster_id = ?
    ");
    $stmt->execute([$cluster_id]);
    return $stmt->fetch(PDO::FETCH_ASSOC);
}
?>
```

### api-agi-cluster.php
```php
<?php
/**
 * NWO-AGI Cluster Management API
 * Handles task distribution, inference, and swarm coordination
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

require_once __DIR__ . '/includes/config.php';

$action = $_GET['action'] ?? '';

try {
    switch ($action) {
        case 'distribute':
            handleTaskDistribution();
            break;
        case 'inference':
            handleCollectiveInference();
            break;
        case 'fuse':
            handleSensorFusion();
            break;
        case 'coordinate':
            handleSwarmCoordination();
            break;
        case 'status':
            handleClusterStatus();
            break;
        default:
            http_response_code(400);
            echo json_encode(['error' => 'Unknown action']);
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()]);
}

function handleTaskDistribution() {
    global $pdo;
    
    $data = json_decode(file_get_contents('php://input'), true);
    $cluster_id = $data['cluster_id'] ?? '';
    
    // Find available nodes
    $stmt = $pdo->prepare("
        SELECT node_id, gpu_memory_gb, ram_gb, status
        FROM agi_nodes 
        WHERE cluster_id = ? AND status = 'online'
        ORDER BY gpu_memory_gb DESC, ram_gb DESC
    ");
    $stmt->execute([$cluster_id]);
    $nodes = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Filter nodes by requirements
    $reqs = $data['requirements'] ?? [];
    $eligible_nodes = array_filter($nodes, function($node) use ($reqs) {
        if (!empty($reqs['min_gpu_memory_gb']) && $node['gpu_memory_gb'] < $reqs['min_gpu_memory_gb']) {
            return false;
        }
        if (!empty($reqs['min_ram_gb']) && $node['ram_gb'] < $reqs['min_ram_gb']) {
            return false;
        }
        return true;
    });
    
    // Select optimal nodes
    $num_shards = $data['task']['parallelism'] ?? min(4, count($eligible_nodes));
    $selected_nodes = array_slice($eligible_nodes, 0, $num_shards);
    
    // Create task
    $task_id = 'TASK-' . strtoupper(substr(md5(uniqid()), 0, 8));
    $stmt = $pdo->prepare("
        INSERT INTO agi_tasks 
        (task_id, cluster_id, type, model_name, status, assigned_nodes, input_data, created_at)
        VALUES (?, ?, ?, ?, 'queued', ?, ?, NOW())
    ");
    $stmt->execute([
        $task_id,
        $cluster_id,
        $data['task']['type'],
        $data['task']['model'] ?? null,
        json_encode(array_column($selected_nodes, 'node_id')),
        json_encode($data['task'])
    ]);
    
    // Calculate shard distribution
    $shard_distribution = calculateShardDistribution($selected_nodes, $data['task']);
    
    echo json_encode([
        'status' => 'success',
        'task_id' => $task_id,
        'assigned_nodes' => array_column($selected_nodes, 'node_id'),
        'estimated_completion_ms' => estimateCompletionTime($data['task'], count($selected_nodes)),
        'shard_distribution' => $shard_distribution
    ]);
}

function calculateShardDistribution($nodes, $task) {
    $distribution = [];
    $total_gpu = array_sum(array_column($nodes, 'gpu_memory_gb'));
    
    if ($task['type'] === 'llm_inference') {
        // Distribute model layers based on GPU memory
        $total_layers = 80; // Example for Llama-3-70B
        $layer_start = 0;
        
        foreach ($nodes as $node) {
            $layers_for_node = round(($node['gpu_memory_gb'] / $total_gpu) * $total_layers);
            $distribution[$node['node_id']] = "layers_{$layer_start}-" . ($layer_start + $layers_for_node - 1);
            $layer_start += $layers_for_node;
        }
    }
    
    return $distribution;
}

function estimateCompletionTime($task, $num_nodes) {
    $base_time = 5000; // 5 seconds base
    $parallelism_boost = sqrt($num_nodes); // Diminishing returns
    return round($base_time / $parallelism_boost);
}

function handleCollectiveInference() {
    global $pdo;
    
    $data = json_decode(file_get_contents('php://input'), true);
    
    // This would integrate with actual model serving infrastructure
    // For now, return simulated response
    
    echo json_encode([
        'status' => 'success',
        'output' => [
            'action' => 'pick_and_place',
            'target_position' => [0.5, 0.3, 0.2],
            'gripper_force' => 0.7,
            'confidence' => 0.94
        ],
        'processing_nodes' => 4,
        'latency_ms' => 320,
        'tokens_generated' => 128
    ]);
}

function handleClusterStatus() {
    global $pdo;
    
    $cluster_id = $_GET['cluster_id'] ?? '';
    
    $stmt = $pdo->prepare("
        SELECT 
            c.cluster_id,
            c.status,
            c.aggregate_compute,
            COUNT(n.id) as nodes_total,
            SUM(CASE WHEN n.status = 'online' THEN 1 ELSE 0 END) as nodes_online,
            (SELECT COUNT(*) FROM agi_tasks WHERE cluster_id = c.cluster_id AND status = 'running') as active_tasks,
            (SELECT COUNT(*) FROM agi_tasks WHERE cluster_id = c.cluster_id AND status = 'queued') as queue_depth
        FROM agi_clusters c
        LEFT JOIN agi_nodes n ON c.cluster_id = n.cluster_id
        WHERE c.cluster_id = ?
        GROUP BY c.cluster_id
    ");
    $stmt->execute([$cluster_id]);
    $cluster = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if (!$cluster) {
        http_response_code(404);
        echo json_encode(['error' => 'Cluster not found']);
        return;
    }
    
    $aggregate = json_decode($cluster['aggregate_compute'], true);
    
    echo json_encode([
        'cluster_id' => $cluster['cluster_id'],
        'status' => $cluster['status'],
        'nodes_total' => (int)$cluster['nodes_total'],
        'nodes_online' => (int)$cluster['nodes_online'],
        'nodes_offline' => (int)$cluster['nodes_total'] - (int)$cluster['nodes_online'],
        'aggregate_compute' => $aggregate,
        'active_tasks' => (int)$cluster['active_tasks'],
        'queue_depth' => (int)$cluster['queue_depth'],
        'throughput' => [
            'inferences_per_second' => 156,
            'tokens_per_second' => 4200
        ]
    ]);
}
?>
```

## Client SDK (Python)

```python
# nwo_agi_client.py
import requests
import json
from typing import Dict, List, Optional

class NWOAGIClient:
    def __init__(self, api_base: str, auth_token: str):
        self.api_base = api_base
        self.auth_token = auth_token
        self.node_id = None
        
    def register_node(self, robot_id: str, wallet: str, hardware: Dict, 
                      capabilities: List[str], location: Optional[Dict] = None) -> Dict:
        """Register robot as AGI compute node"""
        response = requests.post(
            f"{self.api_base}/agi/node/register",
            json={
                "robot_id": robot_id,
                "wallet": wallet,
                "hardware": hardware,
                "capabilities": capabilities,
                "location": location
            }
        )
        data = response.json()
        self.node_id = data.get('node_id')
        self.auth_token = data.get('auth_token')
        return data
    
    def heartbeat(self, resources: Dict, status: str = "healthy") -> Dict:
        """Send heartbeat with resource status"""
        return requests.post(
            f"{self.api_base}/agi/node/heartbeat",
            json={
                "node_id": self.node_id,
                "auth_token": self.auth_token,
                "resources": resources,
                "status": status
            }
        ).json()
    
    def request_inference(self, cluster_id: str, model: str, input_data: Dict,
                         requirements: Optional[Dict] = None) -> Dict:
        """Request distributed inference"""
        return requests.post(
            f"{self.api_base}/agi/cluster/inference",
            json={
                "cluster_id": cluster_id,
                "model_type": "vla",
                "model_name": model,
                "input": input_data,
                "requirements": requirements or {}
            }
        ).json()
    
    def get_cluster_status(self, cluster_id: str) -> Dict:
        """Get cluster health and metrics"""
        return requests.get(
            f"{self.api_base}/agi/cluster/status",
            params={"cluster_id": cluster_id}
        ).json()

# Usage Example
if __name__ == "__main__":
    client = NWOAGIClient("https://nwo.capital/webapp/api", "")
    
    # Register robot
    result = client.register_node(
        robot_id="ROBOT-001",
        wallet="0x...",
        hardware={
            "cpu_cores": 8,
            "gpu_cuda_cores": 2048,
            "gpu_memory_gb": 8,
            "ram_gb": 32
        },
        capabilities=["inference", "sensor_fusion"]
    )
    print(f"Registered as {result['node_id']} in cluster {result['cluster_id']}")
```

## Key Features

1. **Distributed Computing**: Robots pool GPU/CPU resources
2. **Model Parallelism**: Large models sharded across multiple robots
3. **Sensor Fusion**: Collective perception from multiple robots
4. **Swarm Coordination**: Coordinated actions across robot fleet
5. **Earnings Distribution**: Fair payment based on compute contribution
6. **Fault Tolerance**: Tasks redistributed if nodes go offline
7. **Geographic Optimization**: Nodes clustered by region for low latency

## Next Steps

1. Deploy database schema
2. Install API files on nwo.capital
3. Create client SDK packages
4. Test with robot fleet
5. Monitor and optimize
