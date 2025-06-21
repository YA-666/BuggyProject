
"""Monitors Prometheus metrics and triggers rollback if thresholds exceeded."""
import time, os, logging, subprocess
import prometheus_client
from prometheus_client import CollectorRegistry
import requests

PROM_ENDPOINT = os.getenv("PROM_URL", "http://prometheus:9090/api/v1/query")
MEM_VIOL_THRESHOLD = int(os.getenv("MEM_VIOL_THRESHOLD", "3"))
CHECK_INTERVAL = int(os.getenv("ROLLBACK_CHECK_INTERVAL", "60"))  # seconds

def query_metric(metric: str):
    r = requests.get(PROM_ENDPOINT, params={"query": metric})
    r.raise_for_status()
    data = r.json()["data"]["result"]
    if data:
        return float(data[0]["value"][1])
    return 0.0

def rollback():
    logging.warning("Triggering automatic rollback …")
    # naive docker‑compose rollback: restart without cache
    subprocess.run(["/usr/local/bin/docker-compose", "restart", "app"], check=False)

def main():
    logging.basicConfig(level=logging.INFO)
    while True:
        try:
            violations = query_metric("memory_diff_violations_total")
            if violations >= MEM_VIOL_THRESHOLD:
                rollback()
        except Exception as e:
            logging.error("Monitor error: %s", e)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
