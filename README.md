
# Synthetic Soul Assistant – Full Scaffold (Magic Rectangle & Tuned Memory)

Generated on 2025-06-21T12:45:23

## Quick Start

```bash
docker compose up --build
```

Create a `.env` file with your OpenAI credentials before running Docker:

```bash
cp .env.example .env
echo OPENAI_API_KEY=your-key >> .env
```

### Endpoints
| Path | Function |
|------|----------|
| `/chat` | Conversational API |
| `/magic-rect` | Inspect 3×3 slot weight matrix |

---


## Shadow‑memory safeguards

Two maintenance scripts are provided to keep hidden state in check.

| Script | Suggested cron | Purpose |
| ------ | -------------- | ------- |
| `maintenance/slot_scrubber.py` | `0 3 * * *` | Clears any lingering slot text so no residue survives a day. |
| `maintenance/memory_diff_audit.py` | `30 3 * * *` | Dumps daily memory snapshot and flags any entries not written via `write_memory`. |

**Docker tip:** Mount a volume at `/audit` so the diff‑audit snapshots persist across container restarts.

Enable cron inside the container or run these via an external scheduler (K8s CronJob, GitHub Actions, etc.).


## Monitoring & Auto‑rollback

| Service | Port | Purpose |
| ------- | ---- | ------- |
| **Prometheus** | 9090 | Scrapes `/metrics` for violations and slot clears |
| **Grafana** | 3000 | Pre‑provisioned dashboard: *Synthetic Soul Audit* |
| **Auto‑rollback monitor** | (cron) | Restarts the `app` service if violations ≥ 3 |

Start everything (`docker compose up --build`) and visit **http://localhost:3000** (default creds `admin / admin`).  
The auto‑rollback monitor can be run as a side‑car, e.g.:

```bash
python maintenance/auto_rollback_monitor.py
```

Environment variables:

| Name | Default | Description |
| ---- | ------- | ----------- |
| `PROM_URL` | `http://prometheus:9090/api/v1/query` | Where to query metrics |
| `MEM_VIOL_THRESHOLD` | `3` | Violations before rollback |
| `ROLLBACK_CHECK_INTERVAL` | `60` | Polling interval in seconds |
