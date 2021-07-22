import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from utils import read_critical_flow

#Default phases: N_S & S_S; N_L & S_L; E_S & W_S; E_L & W_L

CYCLE = 90 #cycle duration in secs
G_SPLIT = []