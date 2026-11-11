"""Core Heartbeat Sentinel implementation."""
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

class AgentStatus(Enum):
    HEALTHY = "HEALTHY"
    SUSPECT = "SUSPECT"
    DEAD = "DEAD"

@dataclass
class AgentRegistration:
    agent_id: str
    expected_interval_s: float
    timeout_s: float
    last_ping: float
    status: AgentStatus = AgentStatus.HEALTHY
    missed_count: int = 0

class HeartbeatSentinel:
    """Tracks heartbeat intervals and isolates dead or zombie agents."""
    
    def __init__(self):
        self.registry: Dict[str, AgentRegistration] = {}

    def register(self, agent_id: str, interval_s: float = 1.0, timeout_s: float = 3.0) -> None:
        self.registry[agent_id] = AgentRegistration(
            agent_id=agent_id,
            expected_interval_s=interval_s,
            timeout_s=timeout_s,
            last_ping=time.time()
        )

    def ping(self, agent_id: str) -> bool:
        if agent_id not in self.registry:
            return False
        reg = self.registry[agent_id]
        reg.last_ping = time.time()
        reg.status = AgentStatus.HEALTHY
        reg.missed_count = 0
        return True

    def check_health(self) -> Dict[str, AgentStatus]:
        now = time.time()
        results = {}
        for agent_id, reg in self.registry.items():
            elapsed = now - reg.last_ping
            if elapsed > reg.timeout_s:
                reg.status = AgentStatus.DEAD
            elif elapsed > reg.expected_interval_s * 1.5:
                reg.status = AgentStatus.SUSPECT
                reg.missed_count += 1
            else:
                reg.status = AgentStatus.HEALTHY
            results[agent_id] = reg.status
        return results

    def reap_dead_agents(self) -> List[str]:
        dead = []
        for agent_id, reg in list(self.registry.items()):
            if reg.status == AgentStatus.DEAD:
                dead.append(agent_id)
                del self.registry[agent_id]
        return dead
