
"""Nightly slot scrubber.

Clears any non-empty slot in Magic Rectangle 9 to avoid 'shadow memory'.
Intended to be run via cron: 0 3 * * * python maintenance/slot_scrubber.py
"""

import logging, datetime
from app.magic_rect import magic_rect

def main():
    cleared = 0
    for idx in range(9):
        if magic_rect.read(idx):
            magic_rect.release(idx)
            cleared += 1
            from app.metrics_exporter import slot_clears
            slot_clears.inc()
    logging.basicConfig(level=logging.INFO)
    logging.info("Slot scrubber run at %s – cleared %d slots", datetime.datetime.utcnow(), cleared)

if __name__ == "__main__":
    main()
