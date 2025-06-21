
import random
DRIVES={"curiosity":0.5,"affiliation":0.5,"consistency":0.5}
def adjust_drives(_): 
    for k in DRIVES:
        DRIVES[k]=min(1.0,max(0.0,DRIVES[k]+random.uniform(-0.05,0.05)))
    return DRIVES.copy()
