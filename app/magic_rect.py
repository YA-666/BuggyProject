
from __future__ import annotations
from typing import Dict, Optional, Tuple, List
import threading

_LOCK = threading.Lock()

class Slot:
    def __init__(self):
        self.text: str = ""
        self.type: Optional[str] = None
        self.weight: float = 0.0

class MagicRect9:
    ROWS = COLS = 3
    def __init__(self):
        self.slots: Dict[int, Slot] = {i: Slot() for i in range(9)}

    def _row_col(self, idx: int) -> Tuple[int, int]:
        return idx // 3, idx % 3

    def _row_sum(self, row:int) -> float:
        return sum(self.slots[i].weight for i in range(9) if self._row_col(i)[0]==row)

    def _col_sum(self, col:int) -> float:
        return sum(self.slots[i].weight for i in range(9) if self._row_col(i)[1]==col)

    def _normalise(self):
        for idx, slot in self.slots.items():
            r,c = self._row_col(idx)
            denom = max(1.0, self._row_sum(r), self._col_sum(c))
            slot.weight = slot.weight/denom if denom else 0.0

    def claim(self, text:str, slot_type:str="generic", weight:float=0.33)->int:
        with _LOCK:
            empty = next((i for i,s in self.slots.items() if s.weight==0.0), None)
            idx = empty if empty is not None else min(self.slots.items(), key=lambda kv: kv[1].weight)[0]
            s=self.slots[idx]
            s.text=text
            s.type=slot_type
            s.weight=weight
            self._normalise()
            return idx

    def read(self, idx:int)->str:
        return self.slots[idx].text

    def release(self, idx:int):
        with _LOCK:
            s=self.slots[idx]
            s.text=""
            s.type=None
            s.weight=0.0
            self._normalise()

    def matrix(self)->List[List[float]]:
        m=[[0.0]*3 for _ in range(3)]
        for idx,slot in self.slots.items():
            r,c=self._row_col(idx)
            m[r][c]=round(slot.weight,3)
        return m

magic_rect = MagicRect9()
