import os, sys, optparse

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    print(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

def run():
    step = 0
    remove_step = -1
    while step < 200:
        traci.simulationStep()
        # print(step)
        vid_new = "999999999"
        tt = -1
        # if vid in traci.vehicle.getIDList() and step >= 120:
        #     traci.vehicle.remove(vid)
        #     print(f"vehicle: {vid} is removed from the network")
        # det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_0")
        # for veh in det_vehs:
        #     print(f"veh: {veh}")
        if step == 10:
            stage = traci.simulation.findRoute("right1C1", "B1A1.100.00")
            route = stage.edges
            tt = stage.travelTime
            # print(type(stage))
            traci.route.add("trip", route)
            
            traci.vehicle.add(vid_new, "trip")
            duration = 10
            traci.vehicle.setStop(vid_new, "C1B1", 50, 1, duration)
            remove_step = tt + duration + 90
        # this one needs to be determined whether using this rule
        if step >= remove_step:
            if vid_new in traci.vehicle.getIDList():
                traci.vehicle.remove(vid_new)

        # print(f"time: {step}")
        step += 1

    traci.close()
    sys.stdout.flush()

if __name__ == "__main__":
    options = get_options()
    print(options)
    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    sumoBinary = 'sumo-gui'
    # traci starts sumo as a subprocess and then this script connects and runs
    cfg = "../networks/grid2/my.sumocfg"
    traci.start([sumoBinary, "-c", cfg,
                             "--tripinfo-output", "tripinfo.xml"])
    run()
    
print("Done!")