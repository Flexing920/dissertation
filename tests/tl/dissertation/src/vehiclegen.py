import os, sys

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

class VehicleGen:
    def __init__(self, netdata, sim_len, scale, mode, conn):
        np.random.seed(11) # remove randomness
        print("__init__")
        self.conn = conn
        self.v_data = None
        self.vehicles_created = 0
        self.netdata = netdata
        ###for generating vehicles
        self.origins = self.netdata['origin']
        self.destinations = self.netdata['destination'] 
        self.add_origin_routes()
        self.scale = scale
        self.sim_len = sim_len
        self.t = 0

        ###determine what function we run every step to 
        ###generate vehicles into sim

        self.gen_vehicles = self.gen_single


    def run(self):
        print("run")

        self.gen_vehicles()
        self.t += 1


    def add_origin_routes(self):
        print("add_origin_routes")

        for origin in self.origins:
            self.conn.route.add(origin, [origin] )

    def gen_single(self):
        print("gen_single")
        
        if self.conn.vehicle.getIDCount() == 0:
            ###if no vehicles in sim, spawn 1 on random link
            veh_spawn_edge = np.random.choice(self.origins)
            self.gen_veh( [veh_spawn_edge] )

    def gen_veh( self, veh_edges ):
        print("gen_veh")

        for e in veh_edges:
            vid = e+str(self.vehicles_created)
            self.conn.vehicle.addFull( vid, e, departLane="best" )
            self.set_veh_route(vid)
            self.vehicles_created += 1

    def set_veh_route(self, veh):
        print("set_veh_route")

        current_edge = self.conn.vehicle.getRoute(veh)[0]
        route = [current_edge]
        while current_edge not in self.destinations:
            next_edge = np.random.choice(self.netdata['edge'][current_edge]['outgoing'])
            route.append(next_edge)
            current_edge = next_edge
        self.conn.vehicle.setRoute( veh, route )    


if __name__ == "__main__":
    netfp = "../networks/single_intersection/single_intersection.net.xml"
    nd = NetworkData(netfp)
    netdata = nd.get_net_data()
    cfg = "../networks/single_intersection/sumo.sumocfg"
    port = 9000
    print(f"port is {port}")
    traci.start(["sumo", "-c", cfg], port=port, label="sim1")
    conn = traci.getConnection("sim1")
    trafficlights = conn.trafficlight.getIDList()
    step = 0
    v = VehicleGen(netdata, 100, 1, "single", conn)


    while step <= 5:
        traci.simulationStep()
        v.run()
        step += 1
        # more traci commands
    traci.close()




