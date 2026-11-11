"""Unit tests for agent-bidirectional-heartbeat-sentinel."""
import time
import unittest
from agent_bidirectional_heartbeat_sentinel.sentinel import HeartbeatSentinel, AgentStatus

class TestHeartbeatSentinel(unittest.TestCase):
    def setUp(self):
        self.sentinel = HeartbeatSentinel()

    def test_register_and_ping(self):
        self.sentinel.register("agent1", interval_s=1.0, timeout_s=3.0)
        self.assertTrue(self.sentinel.ping("agent1"))
        self.assertEqual(self.sentinel.check_health()["agent1"], AgentStatus.HEALTHY)

    def test_timeout_transition_to_dead(self):
        self.sentinel.register("agent_fast", interval_s=0.05, timeout_s=0.1)
        time.sleep(0.15)
        health = self.sentinel.check_health()
        self.assertEqual(health["agent_fast"], AgentStatus.DEAD)
        reaped = self.sentinel.reap_dead_agents()
        self.assertIn("agent_fast", reaped)
