
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.magic_rect import magic_rect

def test_claim_release():
    idx=magic_rect.claim("unit test","test")
    assert magic_rect.read(idx)=="unit test"
    magic_rect.release(idx)
    assert magic_rect.read(idx)==""
