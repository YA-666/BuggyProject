
import os
IMPORTANCE_THRESHOLD = float(os.getenv("MEM_IMPORTANCE_THRESHOLD", "0.35"))
MAX_TOKENS = int(os.getenv("MEM_MAX_TOKENS", "256"))
RECENCY_TAU = float(os.getenv("MEM_RECENCY_TAU_SECONDS", str(7*24*3600)))
