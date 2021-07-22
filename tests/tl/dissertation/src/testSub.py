import os, sys
import multiprocessing

if 'SUMO_HOME' in os.environ:
   tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
   sys.path.append(tools)
   from sumolib import checkBinary
else:
   sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import sumolib
import numpy as np
from networkdata import NetworkData

def sumo(net):
   pass

if __name__ == "__main__":
    
   cfg = "../networks/single_intersection/sumo.sumocfg"
   net = "../networks/single_intersection/single_intersection.net.xml"

   nd = NetworkData(net)
   netdata = nd.get_net_data()
   # print(nd.find_origin_edges())




