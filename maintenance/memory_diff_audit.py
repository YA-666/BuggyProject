
"""Daily memory diff audit.

Exports top-k memories, hashes them, compares with yesterday's snapshot, and
logs any new entries that did not come from write_memory.
Schedule via cron: 30 3 * * * python maintenance/memory_diff_audit.py
"""

import json, hashlib, datetime, logging, pathlib, sys
from app.memory import read_memory

AUDIT_DIR = pathlib.Path("/audit")  # volume‑mapped for persistence
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

def snapshot():
    memories = read_memory("*", top_k=1000)
    blob = json.dumps(memories, ensure_ascii=False, sort_keys=True)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    fp = AUDIT_DIR / f"{ts}.json"
    fp.write_text(blob)
    return digest, fp

def diff(prev_fp: pathlib.Path, current_memories):
    prev = json.loads(prev_fp.read_text())
    new = [m for m in current_memories if m not in prev]
    return new

def main():
    logging.basicConfig(level=logging.INFO)
    digest, fp = snapshot()
    yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    prev_fp = AUDIT_DIR / f"{yesterday}.json"
    if prev_fp.exists():
        new_items = diff(prev_fp, json.loads(fp.read_text()))
        if new_items:
            from app.metrics_exporter import memory_violations
        memory_violations.inc(len(new_items))
        logging.warning("Detected %d untracked memories: %s", len(new_items), new_items[:5])
        else:
            logging.info("No untracked memories detected.")
    logging.info("Memory diff audit complete – digest %s", digest)

if __name__ == "__main__":
    main()
