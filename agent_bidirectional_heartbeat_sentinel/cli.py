"""CLI for agent-bidirectional-heartbeat-sentinel."""
import sys
import argparse
from .sentinel import HeartbeatSentinel, AgentStatus

def main():
    parser = argparse.ArgumentParser(description="Agent Bidirectional Heartbeat Sentinel CLI")
    parser.add_argument("--demo", action="store_true", help="Simulate agent heartbeat and reaper")
    args = parser.parse_args()

    if args.demo:
        sentinel = HeartbeatSentinel()
        sentinel.register("worker_alpha", interval_s=0.1, timeout_s=0.3)
        sentinel.ping("worker_alpha")
        health = sentinel.check_health()
        print(f"Active health: {health}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
